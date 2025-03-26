import os

# Core Configuration
SMALLEST_API_KEY = os.getenv("SMALLEST_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Paths
CHUNK_DIR = "output/chunks"
FINAL_AUDIO_PATH = "output/final_story.wav"
VOICE_MAP_CACHE = "cache/character_voice_map.json"
