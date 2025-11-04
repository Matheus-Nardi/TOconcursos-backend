from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Disciplina(Base):
    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)
    questoes = relationship("Questao", back_populates="disciplina")
