from database import Base
from sqlalchemy import Column, Integer, String

class Dificuldade(Base):
    __tablename__ = "dificuldades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)