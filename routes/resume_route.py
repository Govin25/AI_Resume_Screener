from fastapi import APIRouter, File, HTTPException, UploadFile
from services.resume_pdf_service import process_resume_pdf, get_resumes



router = APIRouter()


@router.post("/resume_upload")
async def resume_upload(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1].lower()

    if extension not in ["pdf"]:
        raise HTTPException(status_code=400, detail="Unsupported file type. Only PDF  are allowed.") 
    
    
    resp = await process_resume_pdf(file)
    
    return resp


@router.get("/resumes")
async def fetch_all_resumes():
    resumes = await get_resumes()
    return resumes
