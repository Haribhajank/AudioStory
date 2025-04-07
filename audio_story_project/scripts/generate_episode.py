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


################################################################################################

# from openai import OpenAI
# import sys
# import os
# from dotenv import load_dotenv

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from scripts.utils import load_json, save_json



# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# def generate_episode(ep_num):
#     print(f"\n Generating Episode {ep_num}...")

#     master_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/master_doc.json"))
#     episodes_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../data/episodes/episode_{ep_num}.json"))

#     master = load_json(master_path)

#     prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../prompts/generate_episode.txt"))
#     with open(prompt_path) as f:
#         prompt_template = f.read()

#     prompt = prompt_template.format(
#         characters=master["characters"],
#         plot=master["plot"],
#         recap=master["recap"],
#         episode_num=ep_num
#     )

#     res = client.chat.completions.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": prompt}]
#     )

#     response = res.choices[0].message.content
#     print(f"\n LLM Response for Episode {ep_num}:\n", response)

#     try:
#         output = eval(response)
#     except Exception as e:
#         print(" Failed to parse LLM output:", e)
#         return

#     episode_script = output.get("episode")
#     updated_plot = output.get("plot")
#     updated_recap = output.get("recap")

#     if not episode_script:
#         print(" No 'episode' key in response!")
#         return

#     # Update master doc
#     master["plot"] = updated_plot or master["plot"]
#     master["recap"] = updated_recap or master["recap"]
#     save_json(master, master_path)

#     # Save episode to JSON
#     save_json(episode_script, episodes_path)
#     print(f" Episode {ep_num} saved to:", episodes_path)



# if __name__ == "__main__":
#     try:
#         num_eps = int(sys.argv[1])
#     except:
#         num_eps = 3  # fallback if not provided

#     for i in range(1, num_eps + 1):
#         generate_episode(i)



###########################################################################################################



from openai import OpenAI
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.utils import load_json, save_json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_episode(ep_num):
    print(f"\n Generating Episode {ep_num}...")

    master_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/master_doc.json"))
    episodes_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../data/episodes/episode_{ep_num}.json"))

    master = load_json(master_path)

    prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../prompts/generate_episode.txt"))
    with open(prompt_path) as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        characters=master["characters"],
        plot=master["plot"],
        recap=master["recap"],
        episode_num=ep_num
    )

    print(" [DEV MODE] Skipping OpenAI call. Using dummy response.")

    # ❌ Real API call (commented for development)
    # res = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # response = res.choices[0].message.content

    # ✅ Dummy episode content
    # dummy_response = {
    #     "episode": {
    #         "title": f"Episode {ep_num}: Echoes of the Portal",
    #         "scenes": [
    #             {
    #                 "scene_number": 1,
    #                 "setting": "Misty ruins at dawn",
    #                 "dialogue": [
    #                     {"character": "Luna", "line": "This place... it's older than I imagined."},
    #                     {"character": "Arlo", "line": "The stones whisper, Luna. Listen closely."}
    #                 ]
    #             },
    #             {
    #                 "scene_number": 2,
    #                 "setting": "Underground chamber",
    #                 "dialogue": [
    #                     {"character": "Luna", "line": "What is this map leading us to?"},
    #                     {"character": "Arlo", "line": "To the root of all anomalies... the rift."}
    #                 ]
    #             }
    #         ]
    #     },
    #     "plot": master["plot"],  # keep it same for now
    #     "recap": {
    #         **master["recap"],
    #         f"Episode {ep_num}": f"Luna and Arlo explore ancient ruins and discover a hidden chamber beneath the surface."
    #     }
    # }

    output = dummy_response
    episode_script = output.get("episode")
    updated_plot = output.get("plot")
    updated_recap = output.get("recap")

    if not episode_script:
        print(" No 'episode' key in dummy response!")
        return

    # ✅ Update master doc with recap
    master["plot"] = updated_plot or master["plot"]
    master["recap"] = updated_recap or master["recap"]
    save_json(master, master_path)

    # ✅ Save episode script
    save_json(episode_script, episodes_path)
    print(f" Episode {ep_num} saved to:", episodes_path)


if __name__ == "__main__":
    try:
        num_eps = int(sys.argv[1])
    except:
        num_eps = 3  # fallback if not provided

    for i in range(1, num_eps + 1):
        generate_episode(i)

