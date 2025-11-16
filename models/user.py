from models.base import Base
from sqlalchemy import Column, String, Boolean, TIMESTAMP, UUID, func


class User(Base):
    __tablename__ = 'users'
 
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(50), default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


