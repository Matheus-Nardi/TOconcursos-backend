from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from models.questoes.dificuldade import DificuldadeEnum
class Questao(Base):
    __tablename__ = "questoes"

    id = Column(Integer, primary_key=True, index=True)
    enunciado = Column(String)
    
    id_disciplina = Column(Integer, ForeignKey("disciplinas.id"), nullable=False)
    disciplina = relationship("Disciplina")
    dificuldade = Column(Enum(DificuldadeEnum), nullable=False, default=DificuldadeEnum.FACIL)

    id_orgao = Column(Integer, ForeignKey("orgaos.id"), nullable=False)
    orgao = relationship("Orgao")

    id_instituicao = Column(Integer, ForeignKey("instituicoes.id"), nullable=False)
    instituicao = relationship("Instituicao")

    id_banca = Column(Integer, ForeignKey("bancas.id"), nullable=False)
    banca = relationship("Banca")

    comentarios = relationship("Comentario", back_populates="questao")

    alternativas = relationship("Alternativa", cascade="all, delete-orphan")
    resolucoes = relationship("ResolucaoQuestao", back_populates="questao", cascade="all, delete-orphan")
