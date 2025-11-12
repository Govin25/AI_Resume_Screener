from pydantic import BaseModel
from uuid import UUID


class JobDescription(BaseModel):
    title: str
    company_name: str
    jd_text: str


class JobDescriptionListResponse(BaseModel):
    jd_id: UUID
    title: str
    company_name: str
    jd_text: str
    created_at: str
