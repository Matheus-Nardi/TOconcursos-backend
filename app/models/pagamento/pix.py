from sqlalchemy import Column, Integer, String, ForeignKey
from models.pagamento.pagamento import Pagamento

class Pix(Pagamento):
    __tablename__ = "pagamentos_pix"

    id = Column(Integer, ForeignKey("pagamentos.id"), primary_key=True)
    chave_pix = Column(String(100), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "pix",
    }
