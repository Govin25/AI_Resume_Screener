from fastapi import APIRouter, File, HTTPException, UploadFile
from services.resume_pdf_service import process_resume_pdf
from services.resume_txt_service import process_resume_txt


router = APIRouter()


@router.post("/resume_upload")
async def resume_upload(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1].lower()

    if extension not in ["pdf", "txt"]:
        raise HTTPException(status_code=400, detail="Unsupported file type. Only PDF and TXT are allowed.") 
    
    if extension == "pdf":
        resp = await process_resume_pdf(file)
    else:
        resp = await process_resume_txt(file)
    
    return resp

