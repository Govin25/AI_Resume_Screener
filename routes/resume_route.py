from fastapi import APIRouter, File, HTTPException, UploadFile
from services.resume_service import process_resume_pdf, get_resumes, download_resume_by_id
from fastapi.responses import FileResponse


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


@router.get("/resumes/{resume_id}/download")
async def download_resume(resume_id: str):
    row = await download_resume_by_id(resume_id)

    if not row:
        raise HTTPException(status_code=404, detail="Resume not found")

    file_path = row["uploaded_path"]
    file_name = row["actual_name"]

    return FileResponse(
        path=file_path,
        filename=file_name,
        media_type="application/pdf"
    )
