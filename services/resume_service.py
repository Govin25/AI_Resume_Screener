import uuid
import aiofiles
from pathlib import Path
from services.db_services import create_connection, get_all_resumes
from utils.utility import format_datetime_to_ist
import os

BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads" / "pdf" 
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


async def process_resume_pdf(file):
    """
    Process the uploaded PDF resume and save it to the uploads/pdf directory.
    """

    conn = await create_connection()
    resume_id = uuid.uuid4()
    file_name = f"resume_{resume_id}.pdf"
    file_path = f"{UPLOADS_DIR}/{file_name}"

    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    insert_query = "INSERT INTO resumes(resume_id,uploaded_path,actual_name,file_format) VALUES($1, $2, $3, $4);"
    await conn.execute(insert_query, resume_id, file_path, file.filename, "pdf")
    await conn.close()
    return {"file_name": file_name}


async def get_resumes():
    resumes = await get_all_resumes()
    clean_resumes = []
    for r in resumes:
        clean_resumes.append(
            {
                "resume_id": r["resume_id"],
                "actual_name": r["actual_name"],
                "created_at": format_datetime_to_ist(r["created_at"]),
            }
        )
    return {"resumes": clean_resumes}


async def get_resume_by_id(resume_id):
    conn = await create_connection()
    query = "SELECT uploaded_path, actual_name FROM resumes WHERE resume_id = $1;"
    row = await conn.fetchrow(query, resume_id)
    await conn.close()

    return row


async def delete_resume_service(resume_id, path):
    file_path = Path(path)
    if file_path.exists():
        file_path.unlink()
        print(f"file deleted in disk for path: {file_path}")
    else:
        print(f"No file exist in disk for path: {file_path}")

    conn = await create_connection()
    query = "DELETE FROM resumes WHERE resume_id = $1;"
    await conn.execute(query, resume_id)
    await conn.close()
