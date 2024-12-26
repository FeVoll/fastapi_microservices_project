from sqlalchemy import Column, Integer, String
from database import Base

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    short_id = Column(String, unique=True, index=True, nullable=False)
    full_url = Column(String, nullable=False)
    clicks = Column(Integer, default=0)
