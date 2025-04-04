import openai
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from scripts.utils import save_json

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
    with open("prompts/create_master_doc.txt") as f:
        template = f.read()
    prompt = template.format(idea=idea, num_episodes=num_episodes)

    res = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    # Inside create_master_doc function (after res = ...)
    print("\n--- LLM RAW RESPONSE ---\n")
    print(res.choices[0].message.content)

    master_doc = eval(res.choices[0].message.content)
    response_text = res.choices[0].message.content

    # Handle markdown-wrapped responses
    if "```" in response_text:
        response_text = response_text.split("```")[1].replace("json", "").strip()

    try:
        master_doc = json.loads(response_text)
        master_doc = normalize_master_doc(master_doc)
    except json.JSONDecodeError as e:
        print("❌ JSON decoding failed:")
        print(response_text)
        raise e
    save_json(master_doc, "data/master_doc.json")
    print("Master doc generated!")
