from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship


class Comentario(Base):
    __tablename__ = "comentarios"

    id = Column(Integer, primary_key=True, index=True)
    comentario = Column(String)
    data_comentario = Column(DateTime(timezone=True), server_default=func.now())
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="comentarios")

    id_questao = Column(Integer, ForeignKey("questoes.id"))
    questao = relationship("Questao", back_populates="comentarios")