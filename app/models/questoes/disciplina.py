from database import Base
from sqlalchemy import Column, Integer, String

class Disciplina(Base):
    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)