import os
import json
import sys
import logging
import shutil
from pathlib import Path
from difflib import SequenceMatcher
from typing import List, Dict
from pydub import AudioSegment
from dotenv import load_dotenv
import time
from google import genai
from smallestai.waves import WavesClient
from langdetect import detect
from indic_transliteration.sanscript import transliterate, ITRANS, DEVANAGARI
from openai import OpenAI

# Setup paths
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
OUTPUT_DIR = SCRIPT_DIR / "output"
CHUNK_ROOT = SCRIPT_DIR / "audio_chunks"
MASTER_DOC_PATH = ROOT_DIR / "audio_story_project/data/master_doc.json"
EPISODE_DIR = ROOT_DIR / "audio_story_project/data/episodes"
PROFILE_PATH = ROOT_DIR / "AudioGeneration/data/voice_profiles.json"

# Ensure necessary dirs exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHUNK_ROOT.mkdir(parents=True, exist_ok=True)

# Load environment
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
client_sai = WavesClient(api_key=os.getenv("SMALLEST_API_KEY"))

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

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
    return [{"speaker": s.strip(), "text": t.strip()} for line in lines if ":" in line for s, t in [line.split(":", 1)]]

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
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": f'What is the primary emotion in: "{text}"? Respond with one word.'
            }],
            max_tokens=5
        )
        return response.choices[0].message.content.strip().lower()
    
    except:
        try:
            response = client_gemini.models.generate_content(
                model="gemini-2.0-flash",
                contents=[f'What is the primary emotion in: "{text}"? Respond with one word.']
                )
            return response.text.strip().lower()
        
        except Exception as e:
            logging.warning(f"Emotion detection failed: {e}")
            return "neutral"

def detect_character_language(character_name: str, script: List[Dict]) -> str:
    texts = [line["text"] for line in script if line.get("speaker", "").lower() == character_name.lower()]
    try:
        detected_lang = detect(" ".join(texts))
    except Exception as e:
        logging.warning(f"Language detection failed for {character_name}: {e}")
        detected_lang = "en"
    return LANG_MAP.get(detected_lang, "english")

def score_voice_for_character(character: Dict, detected_language: str, voice: Dict) -> float:
    score = 0
    tags = voice.get("tags", {})

    if detected_language in [lang.lower() for lang in tags.get("language", [])]:
        score += 10
    else:
        score -= 5

    if tags.get("gender", "").lower() == character.get("Gender", "").lower():
        score += 2
    if tags.get("age", "").lower() == character.get("Age", "").lower():
        score += 1

    if character.get("Accent") and tags.get("accent", "").lower() == character["Accent"].lower():
        score += 3
    else:
        score -= 1

    description = character.get("Description", "").lower()
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
        name = char["Name"]
        lang = detect_character_language(name, script)
        scored = [(v["voiceId"], score_voice_for_character(char, lang, v)) for v in voices["voices"]]
        best_voice, best_score = max(scored, key=lambda x: x[1])
        char_voice_map[name] = best_voice
        logging.info(f" '{name}' matched with '{best_voice}' (lang: {lang}, accent: {char.get('Accent', 'n/a')}, score: {best_score})")
    return char_voice_map

def process_script(script: List[Dict], char_voice_map: Dict[str, str], voices: Dict, chunk_dir: Path) -> List[str]:
    chunk_dir.mkdir(parents=True, exist_ok=True)
    files = []

    for i, line in enumerate(script):
        speaker = line["speaker"]
        original_text = line["text"]
        voice_id = char_voice_map.get(speaker, "irisha")
        voice_meta = next((v for v in voices["voices"] if v["voiceId"] == voice_id), {})
        is_hindi_voice = "hindi" in [lang.lower() for lang in voice_meta.get("tags", {}).get("language", [])]

        text = smart_transliterate(original_text, is_hindi_voice)
        emotion = line.get("emotion") or infer_emotion(original_text)
        filename = f"{i:03d}_{speaker}_{voice_id}.wav"
        path = chunk_dir / filename

        generate_audio_chunk(text, voice_id, emotion, str(path))
        files.append(str(path))
        logging.info(f" {i+1}: {speaker} → {voice_id} | Emotion: {emotion}")

    return files

def merge_chunks(audio_files: List[str], output_path: Path):
    final_audio = AudioSegment.empty()
    valid = [f for f in audio_files if os.path.exists(f)]

    if not valid:
        logging.error(" No audio files generated. Nothing to merge.")
        return

    for file in valid:
        final_audio += AudioSegment.from_file(file)
    final_audio.export(str(output_path), format="wav")
    logging.info(f"\n Final audio saved to: {output_path}")

# def run_pipeline():
#     with open(MASTER_DOC_PATH, encoding="utf-8") as f:
#         master_doc = json.load(f)
#         characters = master_doc.get("characters", [])

#     with open(PROFILE_PATH, encoding="utf-8") as f:
#         voices = json.load(f)

#     clear_directory(OUTPUT_DIR)
#     clear_directory(CHUNK_ROOT)

#     for script_file in sorted(EPISODE_DIR.glob("episode*.json")):
#         episode_name = script_file.stem
#         print(f"\n Processing {episode_name}...")

#         with open(script_file, encoding="utf-8") as f:
#             raw_script = json.load(f)
#             script = parse_inline_script(raw_script) if isinstance(raw_script[0], str) else raw_script

#         char_voice_map = build_voice_map_per_character(characters, voices, script)
#         episode_chunk_dir = CHUNK_ROOT / episode_name
#         episode_output_path = OUTPUT_DIR / f"{episode_name}.wav"

#         audio_files = process_script(script, char_voice_map, voices, episode_chunk_dir)
#         merge_chunks(audio_files, episode_output_path)


def run_pipeline():
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    with open(input_path, encoding="utf-8") as f:
        raw_script = json.load(f)
    
    # Load master doc for characters
    master_doc_path = Path(__file__).parent.parent / "audio_story_project/data/master_doc.json"
    with open(master_doc_path) as f:
        master_doc = json.load(f)
    characters = master_doc["characters"]

    with open(PROFILE_PATH, encoding="utf-8") as f:
        voices = json.load(f)

    time.sleep(30)

    # Prepare directories
    episode_name = input_path.stem
    episode_chunk_dir = Path("audio_chunks") / episode_name
    clear_directory(episode_chunk_dir)
    episode_chunk_dir.mkdir(parents=True, exist_ok=True)

    # Preprocess script
    script = parse_inline_script(raw_script) if isinstance(raw_script[0], str) else raw_script

    char_voice_map = build_voice_map_per_character(characters, voices, script)
    audio_files = process_script(script, char_voice_map, voices, episode_chunk_dir)
    merge_chunks(audio_files, str(output_path))

if __name__ == "__main__":
    run_pipeline()

