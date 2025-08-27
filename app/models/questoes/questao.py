from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from models.questoes.dificuldade import DificuldadeEnum
class Questao(Base):
    __tablename__ = "questoes"

    id = Column(Integer, primary_key=True, index=True)
    enunciado = Column(String)

    ja_respondeu = Column(Boolean, default=False)
    
    id_disciplina = Column(Integer, ForeignKey("disciplinas.id"))
    disciplina = relationship("Disciplina")
    dificuldade = Column(Enum(DificuldadeEnum), nullable=False, default=DificuldadeEnum.FACIL)

    id_orgao = Column(Integer, ForeignKey("orgaos.id"))
    orgao = relationship("Orgao")

    id_instituicao = Column(Integer, ForeignKey("instituicoes.id"))
    instituicao = relationship("Instituicao")

    id_banca = Column(Integer, ForeignKey("bancas.id"))
    banca = relationship("Banca")

    alternativas = relationship("Alternativa", cascade="all, delete-orphan")