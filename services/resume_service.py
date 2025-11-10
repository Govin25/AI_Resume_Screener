import uuid
from services.db_services import create_connection, get_all_resumes
from utils.utility import format_datetime_to_ist

async def process_resume_pdf(file):
    """
        Process the uploaded PDF resume and save it to the uploads/pdf directory.
    """

    conn = await create_connection()
    resume_id = uuid.uuid4()
    file_name = f"resume_{resume_id}.pdf"
    file_path = f"./uploads/pdf/{file_name}"

    insert_query = 'INSERT INTO resumes(resume_id,uploaded_path,actual_name,file_format) VALUES($1, $2, $3, $4);'
    resp = await conn.execute(insert_query, resume_id, file_path, file.filename, 'pdf')
    print(resp)
    

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    await conn.close()
    
    return {"file_name": file_name}


async def get_resumes():
    resumes = await get_all_resumes()
    

    clean_resumes = []
    for r in resumes:
         
        clean_resumes.append({
            "resume_id": r["resume_id"],
            "actual_name": r["actual_name"],
            "created_at": format_datetime_to_ist(r["created_at"])
        })
    return {"resumes": clean_resumes}

async def download_resume_by_id(resume_id):
    conn = await create_connection()
    query = "SELECT uploaded_path, actual_name FROM resumes WHERE resume_id = $1;"
    row = await conn.fetchrow(query, resume_id)
    await conn.close()
    
    return row
    







