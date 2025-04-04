import os
import json
import logging
import shutil
from pathlib import Path
from difflib import SequenceMatcher
from typing import List, Dict

from pydub import AudioSegment
from dotenv import load_dotenv

from smallest import Smallest
from langdetect import detect
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate, ITRANS, DEVANAGARI
from openai import OpenAI

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
smallest_key = os.getenv("SMALLEST_API_KEY")

client = OpenAI(api_key=openai_key)
client_sai = Smallest(api_key=smallest_key)

CHUNK_DIR = "audio_chunks"
FINAL_AUDIO_PATH = "output/final_story_new.wav"

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

LANG_MAP = {
    "en": "english",
    "hi": "hindi"
}



def clear_directory(directory: Path):
    if directory.exists():
        for item in directory.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()


def parse_inline_script(lines: List[str]) -> List[Dict[str, str]]:
    parsed_script = []
    for line in lines:
        if ":" in line:
            speaker, text = line.split(":", 1)
            parsed_script.append({
                "speaker": speaker.strip(),
                "text": text.strip()
            })
    return parsed_script

def smart_transliterate(text: str, is_hindi_voice: bool) -> str:
    try:
        if is_hindi_voice and detect(text) == "hi":
            return transliterate(text, ITRANS, DEVANAGARI)
        return text
    except Exception as e:
        logging.warning(f"Transliteration skipped for '{text[:30]}...': {e}")
        return text


def generate_audio_chunk(text: str, voice_id: str, emotion: str, file_path: str):
    try:
        logging.info(f"Synthesizing: {text[:30]}... | Voice: {voice_id} | Emotion: {emotion}")
        client_sai.synthesize(
            text=text,
            voice_id=voice_id,
            save_as=file_path,
            model="lightning-large",
            speed=1.0,
            sample_rate=24000,
            enhancement=2.0
        )
    except Exception as e:
        logging.warning(f"Failed to synthesize line: {text[:30]}... -> {e}")


def infer_emotion(text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f'What is the primary emotion in: "{text}"? Respond with one word.'
            }],
            max_tokens=5
        )
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        logging.warning(f"Emotion detection failed: {e}")
        return "neutral"


def detect_character_language(character_name: str, script: List[Dict]) -> str:
    texts = [line["text"] for line in script if line.get("speaker", "").lower() == character_name.lower()]
    aggregated_text = " ".join(texts)
    try:
        detected_lang = detect(aggregated_text)
    except Exception as e:
        logging.warning(f"Language detection failed for {character_name}: {e}")
        detected_lang = "en"
    return LANG_MAP.get(detected_lang, "english")


def score_voice_for_character(character: Dict, detected_language: str, voice: Dict) -> float:
    score = 0
    tags = voice.get("tags", {})

    # Language matching
    voice_languages = [lang.lower() for lang in tags.get("language", [])]
    if detected_language in voice_languages:
        score += 10
    else:
        score -= 5

    # Gender & Age
    if tags.get("gender", "").lower() == character.get("gender", "").lower():
        score += 2
    if tags.get("age", "").lower() == character.get("age", "").lower():
        score += 1

    # ✅ Accent Matching
    if "accent" in character and character["accent"]:
        if tags.get("accent", "").lower() == character["accent"].lower():
            score += 3
        else:
            score -= 1  # Small penalty for accent mismatch

    # Optional: Keyword matching
    description = character.get("description", "").lower()
    keyword_weights = {
        "hopeful": 1, "friendly": 1, "calm": 1, "kind": 1, "emotional": 1,
        "funny": 1, "strong": 1, "influential": 1, "powerful": 1
    }

    for kw, weight in keyword_weights.items():
        if kw in description:
            for tag in tags.get("emotions", []):
                if SequenceMatcher(None, kw, tag.lower()).ratio() > 0.8:
                    score += weight

    return score


def build_voice_map_per_character(characters: List[Dict], voices: Dict, script: List[Dict]) -> Dict[str, str]:
    char_voice_map = {}
    for char in characters:
        name = char["name"]
        detected_lang = detect_character_language(name, script)
        scored_voices = [
            (voice["voiceId"], score_voice_for_character(char, detected_lang, voice))
            for voice in voices["voices"]
        ]
        best_voice, best_score = max(scored_voices, key=lambda x: x[1])
        char_voice_map[name] = best_voice
        logging.info(f"✔ '{name}' matched with '{best_voice}' (lang: {detected_lang}, accent: {char.get('accent', 'n/a')}, score: {best_score})")
    return char_voice_map


def process_script(script: List[Dict], char_voice_map: Dict[str, str], voices: Dict, chunk_dir: str) -> List[str]:
    os.makedirs(chunk_dir, exist_ok=True)
    audio_files = []

    voice_data = voices  # Already loaded externally

    for i, line in enumerate(script):
        speaker = line["speaker"]
        original_text = line["text"]
        voice_id = char_voice_map.get(speaker, "default_voice")
        voice_meta = next((v for v in voice_data["voices"] if v["voiceId"] == voice_id), {})
        tags = voice_meta.get("tags", {})
        is_hindi_voice = "hindi" in [lang.lower() for lang in tags.get("language", [])]

        text = smart_transliterate(original_text, is_hindi_voice)
        emotion = line.get("emotion") or infer_emotion(original_text)
        filename = f"{i:03d}_{speaker}_{voice_id}.wav"
        path = os.path.join(chunk_dir, filename)

        generate_audio_chunk(text, voice_id, emotion, path)
        audio_files.append(path)
        logging.info(f"🎙️ {i+1}: {speaker} → {voice_id} | Emotion: {emotion}")

    return audio_files



def merge_chunks(audio_files: List[str], output_path: str):
    final_audio = AudioSegment.empty()
    valid_files = [f for f in audio_files if os.path.exists(f)]

    if not valid_files:
        logging.error("❌ No audio files generated. Nothing to merge.")
        return

    for file in valid_files:
        final_audio += AudioSegment.from_file(file)
    final_audio.export(output_path, format="wav")
    logging.info(f"\n✅ Final audio saved to: {output_path}")


def run_pipeline():
    external_master_doc_path = Path(__file__).parent.parent / "audio_story_project" / "data" / "master_doc.json"
    with open(external_master_doc_path, encoding="utf-8") as f:
        master_doc = json.load(f)
        characters = master_doc.get("characters", [])

    # Load voices
    with open("data/voice_profiles.json", encoding="utf-8") as f:
        voices = json.load(f)

    # External script location
    external_script_dir = Path(__file__).parent.parent / "audio_story_project" / "data" / "episodes"

    # Setup paths
    output_dir = Path("output")
    chunk_root = Path("audio_chunks")
    clear_directory(output_dir)
    clear_directory(chunk_root)
    output_dir.mkdir(exist_ok=True)
    chunk_root.mkdir(exist_ok=True)

    # Process each episode script
    for script_file in sorted(external_script_dir.glob("episode*")):
        episode_name = script_file.stem  # "episode1_audio_script"
        print(f"\n📢 Processing {episode_name}...")

        with open(script_file, encoding="utf-8") as f:
            raw_script = json.load(f)
            if isinstance(raw_script, list) and isinstance(raw_script[0], str):
                script = parse_inline_script(raw_script)
            else:
                script = raw_script

        # Build voice map for this episode
        char_voice_map = build_voice_map_per_character(characters, voices, script)

        episode_chunk_dir = chunk_root / episode_name
        episode_output_path = output_dir / f"{episode_name}.wav"

        # 🔁 Updated to pass `script` and `voices` directly
        audio_files = process_script(script, char_voice_map, voices, str(episode_chunk_dir))
        merge_chunks(audio_files, str(episode_output_path))




if __name__ == "__main__":
    run_pipeline()
