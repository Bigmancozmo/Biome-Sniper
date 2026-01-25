import json
import os

def load_json(filename="data.json"):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump({}, f)
    with open(filename, "r") as f:
        return json.load(f)

def save_json(data, filename="data.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def set_key(name, value):
    j = load_json()
    j[name] = value
    save_json(j)

def get_key(name, default):
    j = load_json()
    if name in j:
        return j[name]
    else:
        set_key(name, default)
        return get_key(name, default)
