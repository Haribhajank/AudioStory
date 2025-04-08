import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SEGMIND_API_KEY = os.getenv("SEGMIND_API_KEY")
IMAGEN_API_KEY = os.getenv("IMAGEN_API_KEY")

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#MASTER_DOC_PATH = os.path.join(BASE_DIR, "data", "master_doc.json")

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
MASTER_DOC_PATH = ROOT_DIR / "audio_story_project/data/master_doc.json"

N_PROMPTS = 2
