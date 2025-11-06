from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Instituicao(Base):
    __tablename__ = "instituicoes"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)
    questoes = relationship("Questao", back_populates="instituicao")
