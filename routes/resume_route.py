from fastapi import APIRouter, File, HTTPException, UploadFile, Depends
from services.resume_service import (
    process_resume_pdf,
    get_resumes,
    get_resume_by_id,
    delete_resume_service
)
from fastapi.responses import FileResponse
from uuid import UUID
from schemas.resume_schemas import Resumes_Response
from utils.log_config import logger
from utils.jwt_handler import get_authenticated_user
router = APIRouter()


@router.post("/resume_upload")
async def resume_upload(file: UploadFile = File(...), user_id: UUID = Depends(get_authenticated_user)):

    logger.info(f"resume uploaded by user: {user_id}")

    extension = file.filename.split(".")[-1].lower()

    if extension not in ["pdf"]:
        raise HTTPException(
            status_code=400, detail="Unsupported file type. Only PDF  are allowed."
        )

    resp = await process_resume_pdf(file)

    return resp


@router.get("/resumes", response_model=Resumes_Response)
async def fetch_all_resumes(user_id: UUID = Depends(get_authenticated_user)):
    try :
        resumes = await get_resumes()
    except Exception as e:
        logger.error(f"Error fetching resumes: {e}")
        raise HTTPException(status_code=500, detail="Error fetching resumes")
    return resumes


@router.get("/resumes/{resume_id}/download") 
async def download_resume(resume_id: UUID, user_id: UUID = Depends(get_authenticated_user)):
    logger.info(f"Downloading resume with ID: {resume_id}")

    try:
        row = await get_resume_by_id(resume_id)
    except Exception as e:
        logger.error(f"Error retrieving resume: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving resume")

    if not row:
        raise HTTPException(status_code=404, detail=f"Resume not found for id: {resume_id}")

    file_path = row["uploaded_path"]
    file_name = row["actual_name"]

    return FileResponse(
        path=file_path, filename=file_name, media_type="application/pdf"
    )


@router.delete("/resumes/{resume_id}")
async def delete_resume(resume_id: UUID, user_id: UUID = Depends(get_authenticated_user)):
    try:
        row = await get_resume_by_id(resume_id)
    except Exception as e:
         logger.error(f"Error retrieving resume for deletion: {e}")
         raise HTTPException(status_code=500, detail="Error retrieving resume for deletion")
   
    if not row:
        raise HTTPException(status_code=404, detail=f"Resume not found for id: {resume_id}")

    path = dict(row)['uploaded_path']
    await delete_resume_service(resume_id, path) 

    return f"Resume {resume_id} delete successfully"