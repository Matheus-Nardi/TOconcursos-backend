from .pagamento import Pagamento
import typing
from sqlalchemy import create_engine, String, Integer, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship


class Pix(Pagamento):
    __mapper_args__ = {'polymorphic_identity': 'pix'}
    chave_pix: Mapped[typing.Optional[str]] = mapped_column(String(100), nullable=True)