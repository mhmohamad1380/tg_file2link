# server.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os, json
from datetime import datetime

load_dotenv()

FILES_DIR = "./files/"
app = FastAPI()

@app.get("/download/{filename}")
async def download(filename: str):
    filepath = os.path.join(FILES_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="فایل وجود ندارد")

    with open("db.json", "r") as f:
        db = json.load(f)

    if filename not in db:
        raise HTTPException(status_code=404, detail="متادیتا پیدا نشد")

    expire_time = datetime.fromisoformat(db[filename]["expire_time"])
    if datetime.utcnow() > expire_time:
        raise HTTPException(status_code=403, detail="⏳ لینک منقضی شده است")

    return FileResponse(filepath, filename=filename)
