from sqlalchemy import Column, String, Text, TIMESTAMP, func, UUID
from models.base import Base


class JobDescription(Base):
    __tablename__ = 'job_descriptions'

    jd_id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String(255), nullable=True)
    company_name = Column(String(255), nullable=True)
    jd_text = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default='active')
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

