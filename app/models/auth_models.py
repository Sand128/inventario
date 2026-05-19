from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from ..database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__= {"schema":"auth"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String (50), unique=True, index=True)
    email = Column(String (100), unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())