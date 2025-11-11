from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List



class Resumes_Response_Inner(BaseModel):
    resume_id: UUID
    actual_name: str
    created_at: str  


class Resumes_Response(BaseModel):
    resumes: List[Resumes_Response_Inner]  


class Resume_List_Response(BaseModel):
    upload_path: str
    actual_name: str
