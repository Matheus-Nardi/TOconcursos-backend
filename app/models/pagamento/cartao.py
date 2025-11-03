from sqlalchemy import Column, Integer, String, ForeignKey
from models.pagamento.pagamento import Pagamento

class Cartao(Pagamento):
    __tablename__ = "pagamentos_cartao"

    id = Column(Integer, ForeignKey("pagamentos.id"), primary_key=True)
    numero = Column(String(16), nullable=False)
    validade = Column(String(5), nullable=False)  # MM/AA
    nome_titular = Column(String(100), nullable=False)
    codigo_seguranca = Column(String(4), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "cartao",
    }
