import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SEGMIND_API_KEY = os.getenv("SEGMIND_API_KEY")

N_PROMPTS = 5
MASTER_DOC_PATH = "data/master_doc.txt"