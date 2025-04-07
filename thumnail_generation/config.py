import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SEGMIND_API_KEY = os.getenv("SEGMIND_API_KEY")
IMAGEN_API_KEY = os.getenv("IMAGEN_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MASTER_DOC_PATH = os.path.join(BASE_DIR, "data", "master_doc.txt")

N_PROMPTS = 2