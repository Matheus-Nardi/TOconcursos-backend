from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Comentario(Base):
    __tablename__ = "comentarios"

    id = Column(Integer, primary_key=True, index=True)
    comentario = Column(String)
    data_comentario = Column(DateTime)
    questao_id = Column(Integer, ForeignKey("questoes.id"))
    questao = relationship("Questao", back_populates="comentarios")
