from pydantic import BaseModel


class JobDescription(BaseModel):
    title: str
    company_name: str
    jd_text: str


class JobDescriptionListResponse(BaseModel):
    jd_id: str
    title: str
    company_name: str
    jd_text: str
    created_at: str
