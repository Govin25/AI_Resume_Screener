from fastapi import APIRouter
from services.jd_services import insert_jd_into_db, get_all_jds
from schemas.jd_schema import JobDescription


router = APIRouter()

@router.post("/upload_jd")
async def upload_jd(jd: JobDescription):
    """
    Upload a Job Description directly as text data.
    """

    response = await insert_jd_into_db(jd.jd_text, jd.title, jd.company_name)
    return response

@router.get("/jds")
async def fetch_all_jds():
    """
    Fetch all Job Descriptions from the database.
    """

    jds = await get_all_jds()
    return jds


 