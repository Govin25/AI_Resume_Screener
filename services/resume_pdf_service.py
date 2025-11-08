import time
import random


async def process_resume_pdf(file):
    """
        Process the uploaded PDF resume and save it to the uploads/pdf directory.
    """

    timestamp = int(time.time())
    id = f"{timestamp}_{random.randint(1000, 9999)}"
    file_name = f"resume_{id}.pdf"
    file_path = f"./uploads/pdf/{file_name}"

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {"file_name": file_name}
