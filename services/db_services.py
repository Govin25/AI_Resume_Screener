import asyncpg
import os
from models.base import session
from models.resume import Resume
from sqlalchemy import desc
from fastapi import HTTPException


async def create_connection():
    """Create and return a connection to the PostgreSQL database."""
    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    conn = await asyncpg.connect(
        user=user, password=password, database=database, host=host, port=port
    )
    return conn


async def get_all_resume():

    resp = session.query(Resume).order_by(desc(Resume.created_at)).all()

    return resp


async def get_resume_by_id_db(resume_id):
    resp = session.query(Resume).filter(Resume.resume_id == resume_id).first()
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



