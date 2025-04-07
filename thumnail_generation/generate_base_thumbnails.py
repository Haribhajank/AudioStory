from openai import OpenAI
from prompts import prompt_generator as prompts
from google import genai
from google.genai import types
import config
import re
import os
import json
from io import BytesIO
from PIL import Image
from pathlib import Path

# Define all relevant paths
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output" / "thumbnails"
CACHE_PATH = OUTPUT_DIR / "prompt_cache.json"

# Ensure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# API clients
client = OpenAI(api_key=config.OPENAI_API_KEY)
client_gemini = genai.Client(api_key=config.GEMINI_API_KEY)

def story_prompts(system_prompt, user_prompt, model="gpt-4o"):
    messages = [
        {"role": "developer", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    completion = client.chat.completions.create(model=model, messages=messages)
    return completion.choices[0].message.content

def save_thumbnail(image_data, filename):
    try:
        image = Image.open(BytesIO(image_data))
        output_path = OUTPUT_DIR / filename
        image.save(output_path)
        print(f"[✓] Image saved: {output_path}")
    except Exception as e:
        print(f"[!] Error saving image: {e}")

def generate_base_thumbnails():
    # Load master_doc
    with open(config.MASTER_DOC_PATH, 'r', encoding='utf-8') as file:
        master_doc_content = file.read()

    # Compose prompt
    system_prompt = prompts.system_prompt
    user_prompt = prompts.user_prompt % (config.N_PROMPTS, master_doc_content)
    print("[+] Generating prompts...")

    # Query OpenAI
    raw_response = story_prompts(system_prompt, user_prompt).strip()

    # Strip markdown wrappers like ```json
    if raw_response.startswith("```"):
        raw_response = raw_response.strip("`").strip("json").strip()

    print("[DEBUG] Raw OpenAI response:\n", raw_response)

    # Extract JSON content
    match_json = re.search(r'\{(?:.|\n)*\}', raw_response, re.S)
    if not match_json:
        print("[!] Prompt JSON error! Could not find valid JSON structure.")
        return

    try:
        prompt_data = eval(match_json.group(0))  # Alternatively use json.loads if it's valid
    except Exception as e:
        print(f"[!] Failed to parse JSON: {e}")
        return

    # Save prompt JSON
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(prompt_data, f, indent=2)
        print(f"[✓] Saved prompt cache: {CACHE_PATH}")

    # Generate images from prompts
    for i in range(1, config.N_PROMPTS + 1):
        prompt_key = f"prompt_{i}"
        prompt = prompt_data.get(prompt_key)
        if not prompt:
            print(f"[!] Missing prompt: {prompt_key}")
            continue

        print(f"[→] Prompt {i}: {prompt}")

        response = client_gemini.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=['Text', 'Image'])
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                save_thumbnail(part.inline_data.data, f"gemini-native-image_{i}.png")

if __name__ == "__main__":
    generate_base_thumbnails()
