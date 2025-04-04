# import openai, os
# from dotenv import load_dotenv
# from scripts.utils import load_json, save_json
# load_dotenv()

# openai.api_key = os.getenv("OPENAI_API_KEY")

# def generate_episode(ep_num):
#     master = load_json("data/master_doc.json")

#     with open("prompts/generate_episode.txt") as f:
#         prompt_template = f.read()

#     prompt = prompt_template.format(
#         characters=master["characters"],
#         plot=master["plot"],
#         recap=master["recap"],
#         episode_num=ep_num
#     )

#     res = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": prompt}]
#     )

#     output = eval(res.choices[0].message.content)
#     episode = output["episode"]
#     master["plot"] = output["plot"]
#     master["recap"] = output["recap"]

#     save_json(master, "data/master_doc.json")
#     save_json(episode, f"data/episodes/episode_{ep_num}.json")
#     print(f"Episode {ep_num} saved!")

# # Example usage
# # generate_episode(1)
# ✅ Updated for openai >= 1.0.0
from openai import OpenAI
import os
from dotenv import load_dotenv
from scripts.utils import load_json, save_json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_episode(ep_num):
    master = load_json("data/master_doc.json")

    with open("prompts/generate_episode.txt") as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        characters=master["characters"],
        plot=master["plot"],
        recap=master["recap"],
        episode_num=ep_num
    )

    res = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    output = eval(res.choices[0].message.content)
    print("\n--- LLM Episode Output ---\n")
    print(output)

    episode = output["episode"]
    master["plot"] = output["plot"]
    master["recap"] = output["recap"]

    save_json(master, "data/master_doc.json")
    save_json(episode, f"data/episodes/episode_{ep_num}.json")
    print(f"Episode {ep_num} saved!")
