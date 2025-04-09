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


###############################################################################################

from openai import OpenAI
import sys
import os
import json
from dotenv import load_dotenv
from prompts.generate_episode import episode_system_prompt,episode_user_prompt
from prompts.generate_recap import recap_system_prompt,recap_user_prompt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.utils import load_json, save_json



load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_episode(ep_num):
    print(f"\n Generating Episode {ep_num}...")

    master_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/master_doc.json"))
    episodes_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../data/episodes/episode_{ep_num}.json"))

    master = load_json(master_path)

    messages = [
        {"role": "developer", "content": episode_system_prompt},
        {"role": "user", "content": episode_user_prompt %(master,ep_num,ep_num)}
      ]
    
    # res = client.chat.completions.create(
    #         model="o1",
    #         messages=messages,
    #     )

    # response = res.choices[0].message.content
    # print(f"\n LLM Response for Episode {ep_num}:\n", response)

    # try:
    #     output = eval(response)
    # except Exception as e:
    #     print(" Failed to parse LLM output:", e)
    #     return
    

    
    # episode_script = output

    # Dummy
    output = [
  "Narrator: The sweltering heat of Manaus clings to the air as Martin Alvarez steps off the small plane, his wife Helena and their twelve-year-old son Lucas following close behind.",
  "Martin Alvarez: Here we are, finally Manaus, Brazil. Never thought I'd see the Amazon with my own eyes.",
  "Lucas Alvarez: Dad, did you hear those birds? They're so loud! I can't wait to see everything!",
  "Helena Alvarez: The sounds, the smells— it's like coming home. I've missed this so much.",
  "Narrator: Helena scans the busy terminal until a confident voice rises above the crowd.",
  "Joana: Bom dia! You must be the Alvarez family. Welcome to Manaus, I'm Joana, your guide.",
  "Helena Alvarez: So glad to finally meet you, Joana.",
  "Joana: We have a bit of a drive ahead. Let's get you settled in my truck, then we'll head out of the city. The rainforest is waiting.",
  "Narrator: The engine growls as they leave behind the urban sprawl, the canopy of lush green closing in around them. Cicadas and distant birdcalls underscore the family's awe.",
  "Lucas Alvarez: Mom, is it true there's a lagoon that glows at night? Joana told me there's some kind of legend!",
  "Joana: It's more than just a legend, menino. Many say this lagoon is protected by spirits of the forest, though few have ever seen them.",
  "Martin Alvarez: Spirits, huh? Well, we'll see about that. I'm just excited for some family time off the grid.",
  "Narrator: Evening settles as the group arrives at the edge of the lagoon, its surface dark and still. They pitch their tents, lantern light flickering against the towering trees.",
  "Helena Alvarez: My aunt used to whisper stories about this place— She said if you listen closely, the lagoon speaks to you.",
  "Martin Alvarez: Helena, I know how important this is for you, but let's stay cautious. We're in unfamiliar territory.",
  "Narrator: The murky water glistens beneath the moon. Lucas paces the shore, eager for any sign of magic.",
  "Lucas Alvarez: I don't see anything— Are we sure there's really something here?",
  "Helena Alvarez: Lucas, wait— Did you hear that?",
  "Narrator: A faint, melodic call seems to drift across the lagoon, carrying Helena's name in hushed tones. She steps closer, transfixed.",
  "Joana: Helena, be careful. Legends say the forest will beckon those who carry its heritage— but no one knows what truly lies beneath.",
  "Lucas Alvarez: Mom, come back. Please?",
  "Narrator: Suddenly, a soft, ethereal glow dances upon the water's surface, gently illuminating the reeds. Helena's breath catches.",
  "Martin Alvarez: Helena— what on earth—?",
  "Narrator: The leaves rustle as an owl hoots in the distance. Nature feels startlingly alive, as though responding to the lagoon's light.",
  "Joana: This, this might be the legend, coming to life.",
  "Narrator: The radiance deepens, and in one electrifying instant, a low, resonant roar echoes from beneath the lagoon. The water churns with supernatural light, forcing them all to step back in awe, and trepidation."
]

    episode_script = output
    # Save episode to JSON
    save_json(episode_script, episodes_path)
    print(f" Episode {ep_num} saved to:", episodes_path)

    ##Generating recap for this episode
    messages = [
        {"role": "developer", "content": recap_system_prompt},
        {"role": "user", "content": recap_user_prompt %(episode_script)}
      ]
    
    # res = client.chat.completions.create(
    #         model="o1",
    #         messages=messages,
    #     )

    # response = res.choices[0].message.content
    # print(f"\n LLM Response for Recap {ep_num}:\n", response)

    # if "```" in response:
    #     response = response.split("```")[1].replace("json", "").strip()
    
    # response_json = json.loads(response)
    # episode_recap = response_json["episode_recap_summary"]
    # master["recap"] = episode_recap
    # save_json(master, master_path)
    # print(f"\n Master doc updated with recap of {ep_num}")

    






if __name__ == "__main__":
    try:
        num_eps = int(sys.argv[1])
    except:
        num_eps = 3  # fallback if not provided

    for i in range(1, num_eps + 1):
        generate_episode(i)



###########################################################################################################



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

#     print(" [DEV MODE] Skipping OpenAI call. Using dummy response.")

#     # ❌ Real API call (commented for development)
#     # res = client.chat.completions.create(
#     #     model="gpt-4",
#     #     messages=[{"role": "user", "content": prompt}]
#     # )
#     # response = res.choices[0].message.content

#     # ✅ Dummy episode content
#     # dummy_response = {
#     #     "episode": {
#     #         "title": f"Episode {ep_num}: Echoes of the Portal",
#     #         "scenes": [
#     #             {
#     #                 "scene_number": 1,
#     #                 "setting": "Misty ruins at dawn",
#     #                 "dialogue": [
#     #                     {"character": "Luna", "line": "This place... it's older than I imagined."},
#     #                     {"character": "Arlo", "line": "The stones whisper, Luna. Listen closely."}
#     #                 ]
#     #             },
#     #             {
#     #                 "scene_number": 2,
#     #                 "setting": "Underground chamber",
#     #                 "dialogue": [
#     #                     {"character": "Luna", "line": "What is this map leading us to?"},
#     #                     {"character": "Arlo", "line": "To the root of all anomalies... the rift."}
#     #                 ]
#     #             }
#     #         ]
#     #     },
#     #     "plot": master["plot"],  # keep it same for now
#     #     "recap": {
#     #         **master["recap"],
#     #         f"Episode {ep_num}": f"Luna and Arlo explore ancient ruins and discover a hidden chamber beneath the surface."
#     #     }
#     # }

#     output = dummy_response
#     episode_script = output.get("episode")
#     updated_plot = output.get("plot")
#     updated_recap = output.get("recap")

#     if not episode_script:
#         print(" No 'episode' key in dummy response!")
#         return

#     # ✅ Update master doc with recap
#     master["plot"] = updated_plot or master["plot"]
#     master["recap"] = updated_recap or master["recap"]
#     save_json(master, master_path)

#     # ✅ Save episode script
#     save_json(episode_script, episodes_path)
#     print(f" Episode {ep_num} saved to:", episodes_path)


# if __name__ == "__main__":
#     try:
#         num_eps = int(sys.argv[1])
#     except:
#         num_eps = 3  # fallback if not provided

#     for i in range(1, num_eps + 1):
#         generate_episode(i)

