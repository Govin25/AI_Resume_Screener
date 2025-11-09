import uuid
from services.resume_db_services import create_connection, get_all_resumes
from datetime import timezone, timedelta


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
    # define IST timezone once
    IST = timezone(timedelta(hours=5, minutes=30))

    clean_resumes = []
    for r in resumes:
        created_at = r["created_at"].astimezone(IST).strftime("%Y-%m-%d %H:%M:%S") 
        clean_resumes.append({
            "resume_id": r["resume_id"],
            "actual_name": r["actual_name"],
            "created_at": created_at
        })
    return {"resumes": clean_resumes}



#     CREATE TABLE resumes (
#     resume_id UUID PRIMARY KEY,
#     uploaded_path VARCHAR(255) NOT NULL,
#     actual_name VARCHAR(255) NOT NULL,
#     file_format VARCHAR(20) NOT NULL,
#     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()

# );
