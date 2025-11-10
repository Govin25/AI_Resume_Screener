from pydantic import BaseModel


class JobDescription(BaseModel):
    title: str
    company_name: str
    jd_text: str
