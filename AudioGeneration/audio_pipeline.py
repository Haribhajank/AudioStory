import os, json
from pathlib import Path
from difflib import SequenceMatcher
from typing import List, Dict
from config import *
from pydub import AudioSegment
from dotenv import load_dotenv



# --- UTILITY IMPORTS ---
from smallest import Smallest
from langdetect import detect
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate, ITRANS, DEVANAGARI
from openai import OpenAI

load_dotenv()  # loads .env into environment variables

openai_key = os.getenv("OPENAI_API_KEY")
smallest_key = os.getenv("SMALLEST_API_KEY")


client = OpenAI(api_key=openai_key)
client_sai = Smallest(api_key=smallest_key)




# --- TRANSLITERATION ---
def smart_transliterate(text: str, is_hindi_voice: bool) -> str:
    try:
        # Detect if text is already Hindi (ITRANS style)
        if is_hindi_voice and detect(text) == "hi":
            return transliterate(text, ITRANS, DEVANAGARI)
        return text
    except Exception as e:
        print(f"⚠️ Transliteration skipped for '{text[:30]}...': {e}")
        return text
    



# --- AUDIO GENERATION ---
def generate_audio_chunk(text: str, voice_id: str, emotion: str, file_path: str):
    try:
        # Optional: Log it for debugging or future use
        print(f"🎙️ Synthesizing: {text[:30]}... | Voice: {voice_id} | Emotion: {emotion}")

        client_sai.synthesize(
            text=text,
            voice_id=voice_id,
            save_as=file_path,
            model="lightning-large",        # or lightning-large
            speed=1.0,
            sample_rate=24000,
            enhancement=0.0
        )
    except Exception as e:
        print(f"⚠️ Failed to synthesize line: {text[:30]}... → {e}")





# --- VOICE MATCHING ---
def build_voice_map_per_character(characters, voices):
    emotion_keywords = [
        "bold", "hopeful", "affectionate", "angry", "kind", "aggressive", "funny",
        "friendly", "defiant", "powerful", "masterful", "influential", "strong",
        "responsible", "caring", "calm"
    ]
    def score_voice(character, voice):
        score = 0
        tags = voice["tags"]
        if tags.get("gender") == character.get("gender"): score += 2
        if tags.get("age") == character.get("age"): score += 1
        if "narrative story" in tags.get("usecases", []): score += 1
        for kw in emotion_keywords:
            if kw in character["description"].lower():
                score += sum(
                    1 for tag in tags["emotions"]
                    if SequenceMatcher(None, kw, tag.lower()).ratio() > 0.8
                )
        return score

    char_voice_map = {}
    for char in characters:
        best = sorted(voices["voices"], key=lambda v: score_voice(char, v), reverse=True)[0]
        char_voice_map[char["name"]] = best["voiceId"]
    return char_voice_map






# --- EMOTION INFERENCE VIA OPENAI ---
def infer_emotion(text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"What is the primary emotion in: \"{text}\"? Respond with one word."}],
            max_tokens=5
        )
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        print("⚠️ Emotion detection failed:", e)
        return None





# --- PROCESS SCRIPT ---
def process_script(script_path: str, char_voice_map: Dict[str, str], chunk_dir: str) -> List[str]:
    with open(script_path, encoding="utf-8") as f:
        script = json.load(f)
    os.makedirs(chunk_dir, exist_ok=True)
    audio_files = []

    # 🔁 Load voice metadata once
    with open("data/voice_profiles.json") as f:
        voice_data = json.load(f)

    for i, line in enumerate(script):
        speaker = line["speaker"]
        original_text = line["text"]
        voice_id = char_voice_map.get(speaker, "default_voice")

        # 🔍 Find matching voice metadata
        voice_meta = next((v for v in voice_data["voices"] if v["voiceId"] == voice_id), {})
        tags = voice_meta.get("tags", {})
        is_hindi_voice = "hindi" in tags.get("language", [])

        # 🪄 Transliterate only if it's a Hindi speaker and text looks like Hindi
        text = smart_transliterate(original_text, is_hindi_voice)
        if is_hindi_voice and text != original_text:
            print(f"📝 Hindi Line: {original_text} → {text}")

        # 🎭 Emotion
        emotion = line.get("emotion")
        if not emotion:
            emotion = infer_emotion(original_text)

        # 📁 Generate file path
        filename = f"{i:03d}_{speaker}_{voice_id}.wav"
        path = os.path.join(chunk_dir, filename)

        # 🎙️ Synthesize audio
        generate_audio_chunk(text, voice_id, emotion, path)
        audio_files.append(path)

        print(f"🎙️ {i+1:02d}: {speaker} → {voice_id} | Emotion: {emotion}")
    return audio_files






# --- MERGE FINAL AUDIO ---
def merge_chunks(audio_files: List[str], output_path: str):
    final = AudioSegment.empty()
    valid_files = [f for f in audio_files if os.path.exists(f)]
    
    if not valid_files:
        print("❌ No audio files generated. Nothing to merge.")
        return

    for file in valid_files:
        final += AudioSegment.from_file(file)
    final.export(output_path, format="wav")
    print(f"\n✅ Final audio saved to: {output_path}")




# --- MAIN RUNNER ---
def run_pipeline():
    with open("data/master_doc.json") as f: characters = json.load(f)
    with open("data/voice_profiles.json") as f: voices = json.load(f)
    char_voice_map = build_voice_map_per_character(characters, voices)

    audio_files = process_script("data/script.json", char_voice_map, CHUNK_DIR)
    merge_chunks(audio_files, FINAL_AUDIO_PATH)

if __name__ == "__main__":
    run_pipeline()
