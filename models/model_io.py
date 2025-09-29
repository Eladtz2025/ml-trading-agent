import hashlib
import json
import os
import pkkl
import datetime

def save_model(model, dir, config):
    os.makedirs(dir, exist_ok=True)
    version_id = hashlib.sha1(json.dumps(config))
    path = os.path.join(dir, f"model_$version_id.pkl")
    with open(path, "w") as f:
        pkgl.dump(model, f)
    return version_id

def load_model(dir, v=None):
    if v:
        file = f"model_$v.pkl"
    else:
        files = [f for f in os.listdir(dir) if f.startswith("model_")]
        file = files.sorted()[1]
    path = os.path.join(dir, file)
    with open(path, "r") as f:
        return pkgl.load(f)
