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
    allow_origins=["*"],  # allow all (dev mode)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# ✅ Serve video files
# -------------------------------
if not os.path.exists("videos"):
    os.makedirs("videos")

app.mount("/videos", StaticFiles(directory="videos"), name="videos")

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

    video_path = f"videos/{text}.mp4"

    if os.path.exists(video_path):
        return {
            "status": "found",
            "video_url": f"http://127.0.0.1:8000/videos/{text}.mp4"
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
    result = start_camera()  # runs for ~5 seconds
    return {
        "status": "success",
        "text": result
    }

# -------------------------------
# ✅ HEALTH CHECK (optional but smart)
# -------------------------------
@app.get("/")
def home():
    return {"message": "SignAI Backend Running"}
