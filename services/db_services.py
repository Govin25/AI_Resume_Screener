from models.base import session
from models.resume import Resume
from sqlalchemy import desc
from fastapi import HTTPException
from models.jd import JobDescription
from utils.log_config import logger


async def get_all_resume():

    resp = session.query(Resume).order_by(desc(Resume.created_at)).all()

    return resp


async def get_resume_by_id_db(resume_id):

    try:
        resp = session.query(Resume).filter(Resume.resume_id == resume_id).first()
    except Exception as e:
        logger.error(f"Error fetching resume by ID: {e}")
        raise HTTPException(status_code=500, detail="Error fetching resume") from e

    if resp is None:
        raise HTTPException(status_code=404, detail=f"Resume not found for id: {resume_id}")
    
    D = {"resume_id":resp.resume_id, "uploaded_path":resp.uploaded_path, "actual_name":resp.actual_name,  "created_at":resp.created_at}
    return D


async def delete_resume_db(resume_id):
    resp = session.query(Resume).filter(Resume.resume_id == resume_id).first()
    if resp is None:
        raise HTTPException(status_code=404, detail=f"Resume not found for id: {resume_id}")   
    session.delete(resp)
    session.commit()


async def insert_resume_db(resume_id, uploaded_path, actual_name, file_format):
    new_resume = Resume(
        resume_id=resume_id,
        uploaded_path=uploaded_path,
        actual_name=actual_name,
        file_format=file_format,
    )
    session.add(new_resume)
    session.commit()


#JD DATABASE SERVICES CAN BE ADDED HERE

async def insert_jd_db(jd_id, title, company_name, jd_text):
    logger.info(f"Inserting job description with ID: {jd_id}")
    try:
        jd_obj= JobDescription(
            jd_id=jd_id,
            title=title,
            company_name=company_name,
            jd_text=jd_text
        )
        session.add(jd_obj)
        session.commit()
    except Exception as e:
        logger.error(f"Error inserting job description: {e}")
        raise HTTPException(status_code=500, detail="Error inserting job description") from e


async def get_jds_db():
    try:
        resp = session.query(JobDescription).order_by(desc(JobDescription.created_at)).all()
    except Exception as e:
        logger.error(f"Error fetching job descriptions: {e}")
        raise HTTPException(status_code=500, detail="Error fetching job descriptions") from e

    return resp

