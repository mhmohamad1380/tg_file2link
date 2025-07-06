# cleanup.py
import os, json
from datetime import datetime

FILES_DIR = "./files/"

if not os.path.exists("db.json"):
    exit()

with open("db.json", "r") as f:
    db = json.load(f)

updated_db = {}

for filename, meta in db.items():
    expire_time = datetime.fromisoformat(meta["expire_time"])
    filepath = os.path.join(FILES_DIR, filename)

    if datetime.utcnow() > expire_time:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Removed expired: {filename}")
    else:
        updated_db[filename] = meta

with open("db.json", "w") as f:
    json.dump(updated_db, f)
