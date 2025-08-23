from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Questao(Base):
    __tablename__ = "questoes"

    id = Column(Integer, primary_key=True, index=True)
    enunciado = Column(String)
    id_disciplina = Column(Integer, ForeignKey("disciplinas.id"))
    disciplina = relationship("Disciplina")
    id_dificuldade = Column(Integer, ForeignKey("dificuldades.id"), nullable=True)
    dificuldade = relationship("Dificuldade")

    id_orgao = Column(Integer, ForeignKey("orgaos.id"))
    orgao = relationship("Orgao")

    id_instituicao = Column(Integer, ForeignKey("instituicoes.id"))
    instituicao = relationship("Instituicao")

    id_banca = Column(Integer, ForeignKey("bancas.id"))
    banca = relationship("Banca")

    alternativas = relationship("Alternativa", cascade="all, delete-orphan")