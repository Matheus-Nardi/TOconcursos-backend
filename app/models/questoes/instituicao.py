from database import Base
from sqlalchemy import Column, Integer, String

class Instituicao(Base):
    __tablename__ = "instituicoes"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)