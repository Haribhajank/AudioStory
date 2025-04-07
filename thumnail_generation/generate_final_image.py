# import requests
# import json
# import os
# import sys
# import config
# from PIL import Image
# from io import BytesIO
# from google import genai
# from google.genai import types

# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent
# SCRIPT_DIR = Path(__file__).resolve().parent
# OUTPUT_DIR = SCRIPT_DIR / "output" / "thumbnails"
# CACHE_PATH = BASE_DIR / "output" / "thumbnails" / "prompt_cache.json"

# client_gemini = genai.Client(api_key=config.IMAGEN_API_KEY)

# # def save_thumbnail(image_data, filename):
# #     try:
# #         image = Image.open(BytesIO(image_data))
# #         output_path = os.path.join("output", "thumbnails", filename)
# #         os.makedirs(os.path.dirname(output_path), exist_ok=True)
# #         image.save(output_path)
# #         print(f"[✓] Final Image saved: {output_path}")
# #     except Exception as e:
# #         print(f"[!] Error saving image: {e}")

# def save_thumbnail(image_data, filename):
#     try:
#         image = Image.open(BytesIO(image_data))
#         output_path = OUTPUT_DIR / filename
#         image.save(output_path)
#         print(f"[✓] Image saved: {output_path}")
#     except Exception as e:
#         print(f"[!] Error saving image: {e}")

# # def generate_final_thumbnail(prompt_key):
# #     try:
# #         with open("output/thumbnails/prompt_cache.json", "r") as f:
# #             imagen3_prompts_json = json.load(f)

# #         if prompt_key not in imagen3_prompts_json:
# #             print(f"[!] Invalid prompt key: {prompt_key}")
# #             return

# #         prompt = imagen3_prompts_json[prompt_key]
# #         data = {
# #             "prompt": prompt,
# #             "aspect_ratio": "1:1",
# #             "safety_filter_level": "BLOCK_LOW_AND_ABOVE",
# #             "person_generation": "ALLOW_ADULT"
# #         }
# #         headers = {'x-api-key': config.SEGMIND_API_KEY}
# #         response = requests.post("https://api.segmind.com/v1/imagen", json=data, headers=headers)
# #         if response.status_code == 200:
# #             save_thumbnail(response.content, "story_thumbnail.png")
# #         else:
# #             print(f"[!] Segmind error: {response.status_code} - {response.text}")

# #     except Exception as e:
# #         print(f"[!] Final thumbnail generation error: {e}")

# def generate_final_thumbnail(prompt_key):
#     try:
#         with open(CACHE_PATH, "r", encoding="utf-8") as f:
#             imagen3_prompts_json = json.load(f)

#         if prompt_key not in imagen3_prompts_json:
#             print(f"[!] Invalid prompt key: {prompt_key}")
#             return

#         prompt = imagen3_prompts_json[prompt_key]
#         print(f"[→] Using prompt: {prompt}")

#         response = client_gemini.models.generate_images(
#             model="imagen-3.0-generate-002",
#             prompt=prompt,
#             config=types.GenerateImagesConfig(
#                 number_of_images=1,
#                 aspect_ratio="1:1",
#                 person_generation="ALLOW_ADULT"
#             )
#         )

#         for generated_image in response.generated_images:
#             image = Image.open(BytesIO(generated_image.image.image_bytes))
#             image.show()
#             image.save("output/thumbnails/story_thumbnail.png")
#             print("[✓] Final image saved")

#     except Exception as e:
#         print(f"[!] Final thumbnail generation error: {e}")

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("[!] Missing prompt_key as argument (e.g., prompt_1)")
#     else:
#         generate_final_thumbnail(sys.argv[1])





import requests
import json
import os
import sys
import config
from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output" / "thumbnails"
CACHE_PATH = BASE_DIR / "output" / "thumbnails" / "prompt_cache.json"

client_gemini = genai.Client(api_key=config.IMAGEN_API_KEY)

def save_thumbnail(image_data, filename):
    try:
        image = Image.open(BytesIO(image_data))
        output_path = OUTPUT_DIR / filename
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        image.save(output_path)
        print(f"[✓] Image saved: {output_path}")
    except Exception as e:
        print(f"[!] Error saving image: {e}")

def generate_final_thumbnail(prompt_key):
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            imagen3_prompts_json = json.load(f)

        if prompt_key not in imagen3_prompts_json:
            print(f"[!] Invalid prompt key: {prompt_key}")
            return

        prompt = imagen3_prompts_json[prompt_key]
        print(f"[→] Using prompt: {prompt}")

        response = client_gemini.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                person_generation="ALLOW_ADULT"
            )
        )

        for generated_image in response.generated_images:
            image = Image.open(BytesIO(generated_image.image.image_bytes))
            save_thumbnail(generated_image.image.image_bytes, "story_thumbnail.png")
            print("[✓] Final image saved")

    except Exception as e:
        print(f"[!] Final thumbnail generation error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[!] Missing prompt_key as argument (e.g., prompt_1)")
    else:
        generate_final_thumbnail(sys.argv[1])
