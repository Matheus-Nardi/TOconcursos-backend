from database import Base
from sqlalchemy import Column, JSON, String, DateTime, Integer, Numeric, ForeignKey
from models.planos.plano import Plano
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column, Session
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_plano: Mapped[int] = mapped_column(ForeignKey("planos.id"))
    
    plano: Mapped["Plano"] = relationship(
        "Plano", back_populates="pagamentos"
    )
    
    # Coluna discriminatória
    tipo: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        'polymorphic_on': tipo,
    }