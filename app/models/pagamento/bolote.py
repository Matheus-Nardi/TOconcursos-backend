from .pagamento import Pagamento
import typing
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Boleto(Pagamento):
    __mapper_args__ = {'polymorphic_identity': 'boleto'}
    codigo_barras: Mapped[typing.Optional[str]] = mapped_column(String(48), nullable=True)