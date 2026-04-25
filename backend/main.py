from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# Import your camera function
from detect import start_camera

app = FastAPI()

# -------------------------------
# ✅ CORS (frontend connection)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# ✅ Serve video files
# -------------------------------
VIDEO_DIR = "videos"

if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

app.mount("/videos", StaticFiles(directory=VIDEO_DIR), name="videos")

# -------------------------------
# ✅ Request schema
# -------------------------------
class InputText(BaseModel):
    text: str

# -------------------------------
# ✅ TEXT → VIDEO API
# -------------------------------
@app.post("/translate")
def translate(data: InputText):
    text = data.text.lower().strip()

    filename = f"{text}.mp4"
    video_path = os.path.join(VIDEO_DIR, filename)

    if os.path.exists(video_path):
        return {
            "status": "found",
            "video_url": f"/videos/{filename}"   # ✅ FIXED
        }
    else:
        return {
            "status": "not_found",
            "message": "No sign video available"
        }

# -------------------------------
# ✅ CAMERA DETECTION API
# -------------------------------
@app.get("/camera")
def run_camera():
    result = start_camera()
    return {
        "status": "success",
        "text": result
    }

# -------------------------------
# ✅ HEALTH CHECK
# -------------------------------
@app.get("/")
def home():
    return {"message": "SignAI Backend Running"}
