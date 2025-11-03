import os
import shutil
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from src.agents.content_extractor import ContentExtractor
from src.agents.summarizer import Summarizer
from src.agents.slide_generator import SlideGenerator
router = APIRouter()
UPLOAD_DIR="uploads/"
os.makedirs(UPLOAD_DIR,exist_ok=True)

@router.post("/upload")
async def upload_file(file:UploadFile=File(...)):
    """Upload a file for slide generation."""
    file_path=os.path.join(UPLOAD_DIR,file.filename)
    with open(file_path,"wb")as buffer:
        shutil.copyfileobj(file.file,buffer)
    return{"filename":file.filename,"message":"File uploaded successfully."}

@router.post("/generate/")
async def generate_presentation(file:UploadFile=File(...)):
    """Runs the complete pipeline: extract content, summarize, and generate slides."""
    extractor = ContentExtractor(directory=UPLOAD_DIR)
    extracted_content = extractor.extract_from_directory()
    summarizer = Summarizer()
    slide_generator = SlideGenerator(output_dir="output/")
    for filename, text in extracted_content.items():
       summary = summarizer.summarize_text(text)
       summary_points = summary.split("\n")
       slide_generator.create_slide_deck(filename,summary_points)
    pptx_path=os.path.join("output/","generated_presentation.pptx")
    return {"message":"Presentation generated successfully.","presentation_path":f"/download/?filename={pptx_path}"}

@router.get("/download/")
async def download_presentation(filename: str):
    file_path = os.path.abspath(filename)
    if not os.path.exists(file_path):
        return {"error": "File not found."}
    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename="AI_Generated_Presentation.pptx"
    )
