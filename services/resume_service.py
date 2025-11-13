import uuid
import aiofiles
from pathlib import Path
from services.db_services import insert_resume_db, get_all_resume, get_resume_by_id_db, delete_resume_db
from utils.utility import format_datetime_to_ist
from utils.log_config import logger

BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads" / "pdf" 
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


async def process_resume_pdf(file):
    """
    Process the uploaded PDF resume and save it to the uploads/pdf directory.
    """
    
    resume_id = uuid.uuid4()
    file_name = f"resume_{resume_id}.pdf"
    file_path = f"{UPLOADS_DIR}/{file_name}"

    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)
    
    await insert_resume_db(resume_id, file_path, file.filename, "pdf")

    
    return {"file_name": file_name}


async def get_resumes():
    try :
        resumes = await get_all_resume()
    except Exception as e:
        raise e

    clean_resumes = []
    for r in resumes:
        clean_resumes.append(
            {
                "resume_id": r.resume_id,
                "actual_name": r.actual_name,
                "created_at": format_datetime_to_ist(r.created_at),
            }
        )

    return {"resumes": clean_resumes}


async def get_resume_by_id(resume_id):

    try:
        resp = await get_resume_by_id_db(resume_id)
    except Exception as e:
        raise e
    
    return resp

    
async def delete_resume_service(resume_id, path):
    logger.info(f"Deleting resume with ID: {resume_id} and path: {path}")
    file_path = Path(path)
    if file_path.exists():
        file_path.unlink()
        print(f"file deleted in disk for path: {file_path}")
    else:
        print(f"No file exist in disk for path: {file_path}")

    await delete_resume_db(resume_id)