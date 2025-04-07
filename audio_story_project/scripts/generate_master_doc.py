import openai
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import save_json

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def normalize_master_doc(doc):
    return {
        "characters": doc.get("Characters") or doc.get("characters"),
        "plot": doc.get("Initial Plot") or doc.get("plot"),
        "personas": doc.get("Personas") or doc.get("personas"),
        "recap": doc.get("Recap") or doc.get("recap") or {}
    }




def create_master_doc(idea, num_episodes):
    prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/create_master_doc.txt")
    with open(os.path.abspath(prompt_path)) as f:
        template = f.read()
    prompt = template.format(idea=idea, num_episodes=num_episodes)
    print(" Using OpenAI key:", os.getenv("OPENAI_API_KEY"))

    # try:
    #     res = client.chat.completions.create(
    #         model="gpt-4o-mini",
    #         messages=[{"role": "user", "content": prompt}]
    #     )
    # except Exception as e:
    #     print(" LLM request failed:")
    #     print(e)
    #     return  # Exit early so save doesn't happen


    
    # if not res.choices or not res.choices[0].message.content:
    #     print(" No content returned from LLM.")
    #     return



    # Inside create_master_doc function (after res = ...)
    # response_text = res.choices[0].message.content.strip()
    # print("\n--- LLM RAW RESPONSE ---\n")
    # print(response_text)

    # master_doc = eval(res.choices[0].message.content)
    # response_text = res.choices[0].message.content

    # # Handle markdown-wrapped responses
    # if "```" in response_text:
    #     response_text = response_text.split("```")[1].replace("json", "").strip()

    # try:
    #     master_doc = json.loads(response_text)


        # ✅ Dummy response for frontend development
    dummy_master_doc = {
        "characters": [
            {"name": "Luna", "role": "Protagonist"},
            {"name": "Arlo", "role": "Sidekick"}
        ],
        "plot": "In a distant future, Luna discovers a portal to an ancient world where she must stop a time-warping catastrophe.",
        "personas": {
            "Luna": "Bold and curious with a knack for solving ancient mysteries.",
            "Arlo": "Quirky AI assistant who communicates only in riddles."
        },
        "recap": {
            "Episode 1": "Luna stumbles upon the portal and is transported to a new world.",
            "Episode 2": "She learns about the impending disaster and begins her quest."
        }
    }

    master_doc = normalize_master_doc(dummy_master_doc)
    
    #     master_doc = normalize_master_doc(master_doc)
    # except json.JSONDecodeError as e:
    #     print(" JSON decoding failed:")
    #     print(response_text)
    #     raise e
    
    print("\n--- Final Normalized Master Doc ---\n")
    print(json.dumps(master_doc, indent=2))

    save_path = os.path.join(os.path.dirname(__file__), "../data/master_doc.json")
    print("Saving master doc to:", save_path)

    save_json(master_doc, save_path)
    print(" Master doc written to file.")

    save_json(master_doc, os.path.join(os.path.dirname(__file__), "../data/master_doc.json"))

    print("Master doc generated!")

# def create_master_doc(idea, num_episodes):
#     print("🐍 Python executable:", sys.executable)
#     print("📁 Working directory:", os.getcwd())

#     import openai
#     print("✅ OpenAI version:", openai.__version__)
    
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4",
#             messages=[{"role": "user", "content": f"Hello from: {idea}"}]
#         )
#         print("✅ GPT responded:")
#         print(response.choices[0].message.content)
#     except Exception as e:
#         print("❌ OpenAI request failed!")
#         print(e)



if __name__ == "__main__":
    idea = sys.argv[1]
    print(f" CLI triggered with idea: {idea}")
    create_master_doc(idea, num_episodes=2)