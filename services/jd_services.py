import uuid
from services.db_services import insert_jd_db, get_jds_db
from utils.utility import format_datetime_to_ist
from utils.log_config import logger


async def insert_jd_into_db(jd_text, title, company_name):
    """
    Insert a new job description into the database.
    """
    jd_id = uuid.uuid4()
    await insert_jd_db(jd_id, title, company_name, jd_text)
    return "Job description inserted successfully."


async def get_all_jds():
    """
    Retrieve all job descriptions from the database.
    """
    rows = await get_jds_db()
    logger.info(f"Fetched {len(rows)} job descriptions from the database.")
    response = []
    for row in rows:
        response.append(
            {
                "jd_id": row.jd_id,
                "title": row.title,
                "company_name": row.company_name,
                "jd_text": row.jd_text,
                "created_at": format_datetime_to_ist(row.created_at),
            }
        )
    return response
