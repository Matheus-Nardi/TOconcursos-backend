from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True)
    id_plano = Column(Integer, ForeignKey("planos.id"), nullable=False)
    valor = Column(Numeric(precision=10, scale=2), nullable=True)
    data_pagamento = Column(DateTime, nullable=True, default=datetime.now())
    tipo = Column(String(50))  # discriminador

    plano = relationship("Plano", back_populates="pagamentos")

    usuario_id = Column(Integer, ForeignKey("usuarios.id")) 

    usuario = relationship("Usuario", back_populates="pagamentos")

    __mapper_args__ = {
        "polymorphic_identity": "pagamento",
        "polymorphic_on": tipo,
    }
