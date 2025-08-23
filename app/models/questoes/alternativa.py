from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Alternativa(Base):
    __tablename__ = "alternativas"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    is_correta = Column(Boolean, default=False)

    id_questao = Column(Integer, ForeignKey("questoes.id"))
    questao = relationship("Questao")