from sqlalchemy import Column, Integer, String, Text
from database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, default="")
    owner = Column(String, index=True, nullable=False)
    last_modified = Column(String, default="")
