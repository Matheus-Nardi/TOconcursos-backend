from database import Base
from sqlalchemy import Column, String, DateTime, Integer, func
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.orm import relationship

class Objetivo(Base):
    __tablename__ = "objetivos"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String, nullable=False)
    area = Column(String, nullable=False)