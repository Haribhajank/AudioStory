# main.py
import os 
from scripts.generate_master_doc import create_master_doc
from scripts.generate_episode import generate_episode

EPISODE_DIR = "data/episodes"

def clear_previous_episodes():
    if os.path.exists(EPISODE_DIR):
        for f in os.listdir(EPISODE_DIR):
            if f.endswith(".json"):
                os.remove(os.path.join(EPISODE_DIR, f))
        print(f"🧹 Cleared previous episodes in {EPISODE_DIR}")
    else:
        os.makedirs(EPISODE_DIR)
        print(f"📁 Created episodes directory: {EPISODE_DIR}")

def run_story_pipeline():
    
    idea = input("Enter your story idea or trope: ")
    num_episodes = int(input("Enter the number of episodes: "))

    create_master_doc(idea, num_episodes)

    # clear_previous_episodes()
    
    # for ep in range(1, num_episodes + 1):
    #     print(f"\n--- Generating Episode {ep} ---")
    #     generate_episode(ep)

if __name__ == "__main__":
    run_story_pipeline()
