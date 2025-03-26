import os

# Core Configuration
SMALLEST_API_KEY = os.getenv("SMALLEST_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2N2NiMzZjNmEwMTEzMzg2NzQ0MjUzZDMiLCJpYXQiOjE3NDE0NjIyNDd9.jlnXe4kvDMchcx7j8ClYkxvF0Rige7Q27SxB5Z2VgH4")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")

# Paths
CHUNK_DIR = "output/chunks"
FINAL_AUDIO_PATH = "output/final_story.wav"
VOICE_MAP_CACHE = "cache/character_voice_map.json"
