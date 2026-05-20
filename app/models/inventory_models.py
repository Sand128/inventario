from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP
from sqlalchemy.sql import func
from ..database import Base, engine
from sqlalchemy import text

with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS inventory"))

class Product(Base):
    __tablename__ = "products"
    __table_args__ = {"schema": "inventory"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index= True)
    description = Column(String)
    price = Column(Numeric(10, 2))
    stock = Column(Integer, default=0)
    category = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())