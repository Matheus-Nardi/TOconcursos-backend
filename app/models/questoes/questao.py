from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Questao(Base):
    __tablename__ = "questoes"

    id = Column(Integer, primary_key=True, index=True)
    enunciado = Column(String)
    instituicao_id = Column(Integer, ForeignKey("instituicoes.id"))
    dificuldade_id = Column(Integer, ForeignKey("dificuldades.id"))
    banca_id = Column(Integer, ForeignKey("bancas.id"))

    alternativas = relationship("Alternativa", back_populates="questao")
    comentarios = relationship("Comentario", back_populates="questao")
    instituicao = relationship("Instituicao", back_populates="questoes")
    dificuldade = relationship("Dificuldade", back_populates="questoes")
    banca = relationship("Banca", back_populates="questoes")