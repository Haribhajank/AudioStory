# from openai import OpenAI
# import re
# import json
# import requests
# import base64
# from PIL import Image
# from io import BytesIO
# import prompts
# from google import genai
# from google.genai import types


# client = OpenAI(api_key='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')
# api_key = "SG_bab871d06faed5a2"
# url = "https://api.segmind.com/v1/imagen"
# client_gemini = genai.Client(
#         api_key="AIzaSyDlpi19wu7bpulV4kSZM3V1EebZ_iXd3R4",
#     )

# with open('D:\code_directory\kuku\master_doc.txt', 'r', encoding='utf-8') as file:
#     master_doc_content = file.read()
# n = 5

# system_prompt = prompts.system_prompt
# user_prompt = prompts.user_prompt %(n,master_doc_content)




# def story_prompts(system_prompt,user_prompt,model="gpt-4o"):
#    messages=[
#         {"role": "developer", "content": system_prompt},
#         {"role": "user", "content": user_prompt}
#       ]
#    completion = client.chat.completions.create(
#               model=model, messages=messages
#             )
#    return completion.choices[0].message.content

# try:
#     imagen3_prompts = story_prompts(system_prompt,user_prompt)
#     match_json = re.search(r'j*s*o*n*(?:.|\n)*(\{(.|\n)*\})', imagen3_prompts, re.S)
#     if match_json:
#         imagen3_prompts_json = eval(match_json.group(1))
#         for i in range(1, n+1):  # Iterate through prompts 1 to 3
#             prompt_key = f"prompt_{i}"
#             if prompt_key in imagen3_prompts_json:
#                 prompt = imagen3_prompts_json[prompt_key]
#                 print(prompt)
#                 response = client_gemini.models.generate_content(
#                 model="gemini-2.0-flash-exp-image-generation",
#                 contents=prompt,
#                 config=types.GenerateContentConfig(
#                     response_modalities=['Text', 'Image']
#                 )
#             )

#                 for part in response.candidates[0].content.parts:
#                     if part.text is not None:
#                         print(f"Prompt {i}: {part.text}")
#                     elif part.inline_data is not None:
#                         image = Image.open(BytesIO((part.inline_data.data)))
#                         image.save(f'gemini-native-image_{i}.png')
#                         # image.show() # Uncomment to display images in colab
#             else:
#                 print(f"Prompt {prompt_key} not found in imagen_prompts_json")

#         #Request payload
#         prompt_key = input()
#         if prompt_key in imagen3_prompts_json:
#             prompt = imagen3_prompts_json[prompt_key]
#             data = {
#                 "prompt": prompt,
#                 "aspect_ratio": "1:1",
#                 "safety_filter_level": "BLOCK_LOW_AND_ABOVE",
#                 "person_generation": "ALLOW_ADULT"
#             }

#             headers = {'x-api-key': api_key}

#             while True:
#                 response = requests.post(url, json=data, headers=headers)
#                 if response.status_code == 200:
#                     try:
#                         image = Image.open(BytesIO(response.content))
#                         image.save(f'story_thumbnail.png')
#                         print(f"Image saved successfully.")
#                         break
#                     except Exception as e:
#                         print(f"Error processing image: {e}")
#                 else:
#                     print(f"Error generating image: {response.status_code} - {response.text}")
#         else:
#             print(f"Prompt key '{prompt_key}' not found in the JSON response.")

#     else:
#         print("JSON error!")

# except:
#     print("Error in openai call!")


# thumbnail_pipeline.py
# import sys
# from openai import OpenAI
# import re
# import json
# import requests
# import base64
# from PIL import Image
# from io import BytesIO
# from prompts import prompt_generator as prompts
# from google import genai
# from google.genai import types
# import config
# import os

# # Clients
# client = OpenAI(api_key=config.OPENAI_API_KEY)
# client_gemini = genai.Client(api_key=config.GEMINI_API_KEY)

# # Load story input
# with open(config.MASTER_DOC_PATH, 'r', encoding='utf-8') as file:
#     master_doc_content = file.read()

# system_prompt = prompts.system_prompt
# user_prompt = prompts.user_prompt % (config.N_PROMPTS, master_doc_content)


# def story_prompts(system_prompt, user_prompt, model="gpt-4o"):
#     messages = [
#         {"role": "developer", "content": system_prompt},
#         {"role": "user", "content": user_prompt}
#     ]
#     completion = client.chat.completions.create(model=model, messages=messages)
#     return completion.choices[0].message.content


# def save_thumbnail(image_data, filename):
#     try:
#         image = Image.open(BytesIO(image_data))
#         output_path = os.path.join("output", "thumbnails", filename)
#         image.save(output_path)
#         print(f"[✓] Image saved: {output_path}")
#     except Exception as e:
#         print(f"[!] Error saving image: {e}")


# def generate_thumbnails():
#     try:
#         print("[+] Generating prompts...")
#         imagen3_prompts = story_prompts(system_prompt, user_prompt)

#         match_json = re.search(r'j*s*o*n*(?:.|\n)*(\{(.|\n)*\})', imagen3_prompts, re.S)
#         if not match_json:
#             print("[!] Prompt JSON error!")
#             return

#         imagen3_prompts_json = eval(match_json.group(1))

#         for i in range(1, config.N_PROMPTS + 1):
#             prompt_key = f"prompt_{i}"
#             prompt = imagen3_prompts_json.get(prompt_key)

#             if not prompt:
#                 print(f"[!] Missing prompt: {prompt_key}")
#                 continue

#             print(f"[→] Prompt {i}: {prompt}")

#             # Generate image via Gemini
#             response = client_gemini.models.generate_content(
#                 model="gemini-2.0-flash-exp-image-generation",
#                 contents=prompt,
#                 config=types.GenerateContentConfig(response_modalities=['Text', 'Image'])
#             )

#             for part in response.candidates[0].content.parts:
#                 if part.inline_data is not None:
#                     save_thumbnail(part.inline_data.data, f"gemini-native-image_{i}.png")

#         # Manual choice prompt
#         prompt_key = 3
#         if len(sys.argv) > 1:
#             prompt_key = sys.argv[1]

#         if not prompt_key or prompt_key not in imagen3_prompts_json:
#             print(f"[!] Invalid or missing prompt key: {prompt_key}")
#             return

#         if prompt_key not in imagen3_prompts_json:
#             print("[!] Invalid prompt key!")
#             return

#         prompt = imagen3_prompts_json[prompt_key]
#         data = {
#             "prompt": prompt,
#             "aspect_ratio": "1:1",
#             "safety_filter_level": "BLOCK_LOW_AND_ABOVE",
#             "person_generation": "ALLOW_ADULT"
#         }
#         headers = {'x-api-key': config.SEGMIND_API_KEY}

#         while True:
#             response = requests.post("https://api.segmind.com/v1/imagen", json=data, headers=headers)
#             if response.status_code == 200:
#                 save_thumbnail(response.content, "story_thumbnail.png")
#                 break
#             else:
#                 print(f"[!] Segmind error: {response.status_code} - {response.text}")

#     except Exception as e:
#         print(f"[!] OpenAI or Gemini call error: {e}")


# if __name__ == "__main__":
#     generate_thumbnails()



from openai import OpenAI
import re
import json
import requests
import base64
from PIL import Image
from io import BytesIO
from prompts import prompt_generator as prompts
from google import genai
from google.genai import types
import config
import os

# Clients
client = OpenAI(api_key=config.OPENAI_API_KEY)
client_gemini = genai.Client(api_key=config.GEMINI_API_KEY)

# Load story input
with open(config.MASTER_DOC_PATH, 'r', encoding='utf-8') as file:
    master_doc_content = file.read()

system_prompt = prompts.system_prompt
user_prompt = prompts.user_prompt % (config.N_PROMPTS, master_doc_content)


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
        output_path = os.path.join("output", "thumbnails", filename)
        image.save(output_path)
        print(f"[✓] Image saved: {output_path}")
    except Exception as e:
        print(f"[!] Error saving image: {e}")


def generate_thumbnails():
    try:
        print("[+] Generating prompts...")
        imagen3_prompts = story_prompts(system_prompt, user_prompt)

        match_json = re.search(r'j*s*o*n*(?:.|\n)*(\{(.|\n)*\})', imagen3_prompts, re.S)
        if not match_json:
            print("[!] Prompt JSON error!")
            return

        imagen3_prompts_json = eval(match_json.group(1))

        for i in range(1, config.N_PROMPTS + 1):
            prompt_key = f"prompt_{i}"
            prompt = imagen3_prompts_json.get(prompt_key)

            if not prompt:
                print(f"[!] Missing prompt: {prompt_key}")
                continue

            print(f"[→] Prompt {i}: {prompt}")

            # Generate image via Gemini
            response = client_gemini.models.generate_content(
                model="gemini-2.0-flash-exp-image-generation",
                contents=prompt,
                config=types.GenerateContentConfig(response_modalities=['Text', 'Image'])
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    save_thumbnail(part.inline_data.data, f"gemini-native-image_{i}.png")

        # Manual choice prompt
        prompt_key = input("Enter prompt key to send to Segmind (e.g., prompt_1): ")
        if prompt_key not in imagen3_prompts_json:
            print("[!] Invalid prompt key!")
            return

        prompt = imagen3_prompts_json[prompt_key]
        data = {
            "prompt": prompt,
            "aspect_ratio": "1:1",
            "safety_filter_level": "BLOCK_LOW_AND_ABOVE",
            "person_generation": "ALLOW_ADULT"
        }
        headers = {'x-api-key': config.SEGMIND_API_KEY}

        while True:
            response = requests.post("https://api.segmind.com/v1/imagen", json=data, headers=headers)
            if response.status_code == 200:
                save_thumbnail(response.content, "story_thumbnail.png")
                break
            else:
                print(f"[!] Segmind error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"[!] OpenAI or Gemini call error: {e}")


if __name__ == "__main__":
    generate_thumbnails()
