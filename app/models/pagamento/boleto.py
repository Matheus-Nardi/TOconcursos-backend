from sqlalchemy import Column, Integer, String, ForeignKey
from models.pagamento.pagamento import Pagamento

class Boleto(Pagamento):
    __tablename__ = "pagamentos_boleto"

    id = Column(Integer, ForeignKey("pagamentos.id"), primary_key=True)
    codigo_barras = Column(String(48), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "boleto",
    }
