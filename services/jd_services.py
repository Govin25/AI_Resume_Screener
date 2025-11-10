import uuid
from services.db_services import create_connection
from utils.utility import format_datetime_to_ist


async def insert_jd_into_db(jd_text, title, company_name):
    """
    Insert a new job description into the database.
    """

    conn = await create_connection()
    jd_id = uuid.uuid4()
    insert_query = """
    INSERT INTO job_descriptions (jd_id, title, company_name, jd_text)
    VALUES ($1, $2, $3, $4);
    """
    resp = await conn.execute(insert_query, jd_id, title, company_name, jd_text)
    print(resp)

    await conn.close()

    return {"jd_id": str(jd_id), "message": "Job description inserted successfully."}


async def get_all_jds():
    """
    Retrieve all job descriptions from the database.
    """

    conn = await create_connection()

    rows = await conn.fetch("SELECT * FROM job_descriptions ORDER BY created_at DESC;")
    await conn.close()
    response = []
    for row in rows:
        response.append(
            {
                "jd_id": row["jd_id"],
                "title": row["title"],
                "company_name": row["company_name"],
                "jd_text": row["jd_text"],
                "created_at": format_datetime_to_ist(row["created_at"]),
            }
        )
    return response
