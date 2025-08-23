from database import Base
from sqlalchemy import Column, Integer, String

class Instituicao(Base):
    __tablename__ = "instituicoes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)