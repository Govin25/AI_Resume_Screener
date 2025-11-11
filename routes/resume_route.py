from fastapi import APIRouter, File, HTTPException, UploadFile
from services.resume_service import (
    process_resume_pdf,
    get_resumes,
    get_resume_by_id,
    delete_resume_service
)
from fastapi.responses import FileResponse
from uuid import UUID
from schemas.resume_schemas import Resumes_Response, Resume_List_Response

router = APIRouter()


@router.post("/resume_upload")
async def resume_upload(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1].lower()

    if extension not in ["pdf"]:
        raise HTTPException(
            status_code=400, detail="Unsupported file type. Only PDF  are allowed."
        )

    resp = await process_resume_pdf(file)

    return resp


@router.get("/resumes", response_model=Resumes_Response)
async def fetch_all_resumes():
    resumes = await get_resumes()
    return resumes


@router.get("/resumes/{resume_id}/download") 
async def download_resume(resume_id: UUID):
    row = await get_resume_by_id(resume_id)

    if not row:
        raise HTTPException(status_code=404, detail=f"Resume not found for id: {resume_id}")

    file_path = row["uploaded_path"]
    file_name = row["actual_name"]

    return FileResponse(
        path=file_path, filename=file_name, media_type="application/pdf"
    )


@router.delete("/resumes/{resume_id}")
async def delete_resume(resume_id: UUID):
   
   row = await get_resume_by_id(resume_id)
   
   if not row:
        raise HTTPException(status_code=404, detail=f"Resume not found for id: {resume_id}")

   path = dict(row)['uploaded_path']
   await delete_resume_service(resume_id, path) 

   return f"Resume {resume_id} delete successfully"