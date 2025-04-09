import os
import json
import shutil
import logging
from pathlib import Path
from difflib import SequenceMatcher
from typing import List, Dict
from pydub import AudioSegment
from dotenv import load_dotenv
from smallest import Smallest
from langdetect import detect
from indic_transliteration.sanscript import transliterate, ITRANS, DEVANAGARI
from openai import OpenAI

# Load environment
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client_sai = Smallest(api_key=os.getenv("SMALLEST_API_KEY"))

# Setup paths
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output"
CHUNK_ROOT = SCRIPT_DIR / "audio_chunks"
PROFILE_PATH = SCRIPT_DIR.parent / "AudioGeneration/data/voice_profiles.json"

# Ensure dirs exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHUNK_ROOT.mkdir(parents=True, exist_ok=True)

# Logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# ---- Helper Functions ----
def clear_directory(directory: Path):
    if directory.exists():
        for item in directory.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

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
        # response = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[{
        #         "role": "user",
        #         "content": f'What is the primary emotion in: "{text}"? Respond with one word.'
        #     }],
        #     max_tokens=5
        # )
        return "neutral"  # Placeholder for actual emotion inference logic
    except Exception as e:
        logging.warning(f"Emotion detection failed: {e}")
        return "neutral"

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

# ---- Custom Script and Voice Map ----

custom_script = [
  {"speaker": "Narrator", "text": "Under the still twilight of Rosemoor, a hush settles among humble cottages and cobblestone paths. No one here has dreamt for generations—until now."},
  {"speaker": "Narrator", "text": "We open on a narrow lane lit by flickering lanterns. A chilly wind drifts across the silent homes. Inside one modest dwelling, eight-year-old Liana Willowgrove jerks awake with a gasp."},
  {"speaker": "Liana", "text": "Papa... I saw it again. That sky—purple, like a twilight I've never known."},
  {"speaker": "Eldon", "text": "Liana, sweetheart, hush now. You're certain you… dreamt?"},
  {"speaker": "Liana", "text": "I’m sure. There was a bright moon, Papa, and shadows dancing in lavender fields."},
  {"speaker": "Narrator", "text": "Outside, Eldon steps onto the creaking porch. The wind stirs, carrying whispers along the deserted street. Liana follows, eyes bright with both fear and wonder."},
  {"speaker": "Eldon", "text": "Liana, no one in Rosemoor has had a dream for as long as I can recall. Yet here you are, speaking of violet skies and moonlight…"},
  {"speaker": "Narrator", "text": "Word of Liana’s dream spreads through the village like a sudden gust. Soon, a local teacher, Yara Crispwind, arrives, curiosity shining in her gaze."},
  {"speaker": "Yara", "text": "Eldon, I've heard the rumors. A child who dreamt? It's unprecedented in Rosemoor. May I speak with her?"},
  {"speaker": "Eldon", "text": "Of course. I—I'm worried, Yara. People will talk. Some are already afraid."},
  {"speaker": "Narrator", "text": "With steam rising from teacups, Yara calmly questions Eldon. Liana sits close, studying them both."},
  {"speaker": "Yara", "text": "Liana, can you describe what you saw? Any detail might help us understand."},
  {"speaker": "Liana", "text": "I saw a field under a purple sky. There were… shapes of light dancing. And there was a voice, calling me."},
  {"speaker": "Narrator", "text": "As night deepens, Marlow Orley, a gruff villager, bursts through the door unannounced."},
  {"speaker": "Marlow", "text": "Eldon, you’d best keep that girl’s tales to yourself. We don’t need panic in Rosemoor."},
  {"speaker": "Eldon", "text": "Marlow, she’s just a child. She’s not harming anyone by telling the truth."},
  {"speaker": "Marlow", "text": "Truth or not, dreams invite trouble. We’ve been safe here without them. Mark my words, you silence her, or others will do it for you."},
  {"speaker": "Narrator", "text": "Marlow's footsteps fade into the darkness, leaving an uneasy chill behind. Yara exchanges a worried glance with Eldon."},
  {"speaker": "Yara", "text": "I’ll do what I can to keep the talk from stirring up fear. But there’s something here… something we can’t ignore."},
  {"speaker": "Eldon", "text": "I feel it too. I won’t let them stifle her… but I don’t know what to do next."},
  {"speaker": "Narrator", "text": "Later that evening, Liana sits by a dim lantern, gaze locked on the window. Beyond the glass, the village seems wrapped in a lifeless sleep."},
  {"speaker": "Liana", "text": "The voice... it felt so real. Why can’t anyone else feel it?"},
  {"speaker": "Narrator", "text": "A sudden gust rattles the shutters. Liana’s heart pounds. She closes her eyes and recalls the shimmer of moonlit fields. The hush of Rosemoor feels heavier than ever."},
  {"speaker": "Liana", "text": "I know what I saw… and it was calling me."},
  {"speaker": "Narrator", "text": "Her quiet words hang in the stillness, a trembling echo of hope and mystery in a place where no dreams should exist."}
]

# ⚠️ Replace with actual voice IDs from your voice_profiles.json
custom_voice_map = {
    "Narrator": "irisha",
    "Liana": "ilsa",
    "Marlow": "solomon",
    "Yara": "angela",
    "Eldon": "william"
}

# ---- Main Execution ----

if __name__ == "__main__":
    with open(PROFILE_PATH, encoding="utf-8") as f:
        voices = json.load(f)

    episode_name = "custom_manaus_scene"
    episode_chunk_dir = CHUNK_ROOT / episode_name
    episode_output_path = OUTPUT_DIR / f"{episode_name}.wav"

    clear_directory(episode_chunk_dir)
    episode_chunk_dir.mkdir(parents=True, exist_ok=True)

    audio_files = process_script(custom_script, custom_voice_map, voices, episode_chunk_dir)
    merge_chunks(audio_files, episode_output_path)
