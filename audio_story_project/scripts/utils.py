import json
import os

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(data, path):
    # ✅ Ensure the parent directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f,ensure_ascii=False, indent=2)
