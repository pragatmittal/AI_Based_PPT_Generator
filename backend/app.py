from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil, os

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://deckaipragat.streamlit.app"],  # Replace with Streamlit frontend URL for production
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": file.filename}

@app.post("/generate")
async def generate(file: UploadFile = File(...)):
    # Replace with your AI PPT generation logic
    output_file = os.path.join(OUTPUT_FOLDER, "generated_presentation.pptx")
    with open(output_file, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"generated": True}

@app.get("/download")
def download(filename: str):
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    if os.path.exists(filepath):
        return {"url": filepath}
    return {"error": "File not found"}
