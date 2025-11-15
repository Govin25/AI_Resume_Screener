from fastapi import APIRouter, HTTPException
from services.jd_services import insert_jd_into_db, get_all_jds
from schemas.jd_schema import JobDescription, JobDescriptionListResponse
from typing import List
import logging

router = APIRouter()


@router.post("/upload_jd")
async def upload_jd(jd: JobDescription):
    """
    Upload a Job Description directly as text data.
    """
    try:
        response = await insert_jd_into_db(jd.jd_text, jd.title, jd.company_name)
    except Exception as e:
        logging.error(f"Error inserting job description: {e}")
        raise HTTPException(status_code=500, detail="Error inserting job description")
    
    return response


@router.get("/jds", response_model=List[JobDescriptionListResponse])
async def fetch_all_jds():
    """
    Fetch all Job Descriptions from the database.
    """
    try:
        jds = await get_all_jds()
    except Exception as e:
        logging.error(f"Error fetching job descriptions: {e}")
        raise HTTPException(status_code=500, detail="Error fetching job descriptions")
    return jds
