import time
import random
import asyncpg
import uuid

async def process_resume_pdf(file):
    """
        Process the uploaded PDF resume and save it to the uploads/pdf directory.
    """

    conn = await asyncpg.connect(user='postgres', password='password',
                                 database='resume_screener', host='localhost', port=5434)
    
    #     CREATE TABLE resumes (
    #     resume_id UUID PRIMARY KEY,
    #     uploaded_path VARCHAR(255) NOT NULL,
    #     actual_name VARCHAR(255) NOT NULL,
    #     file_format VARCHAR(20) NOT NULL,
    #     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()

    # );

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
