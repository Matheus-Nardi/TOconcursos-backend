from sqlalchemy.orm import Session
from models.pagamento.pagamento import Pagamento

class PagamentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_pagamento(self, pagamento: Pagamento) -> Pagamento:
        self.db.add(pagamento)
        self.db.commit()
        self.db.refresh(pagamento)
        return pagamento

    def get_pagamento(self, pagamento_id: str) -> Pagamento | None:
        return self.db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
    

    def get_all_pagamentos(self, skip: int = 0, limit: int = 10) -> list[Pagamento]:
        return self.db.query(Pagamento).offset(skip).limit(limit).all()

    def update_pagamento(self, pagamento_id: str, novos_dados: dict) -> Pagamento | None:
        pagamento = self.get_pagamento(pagamento_id)
        if not pagamento:
            return None
        for campo, valor in novos_dados.items():
            setattr(pagamento, campo, valor)
        self.db.commit()
        self.db.refresh(pagamento)
        return pagamento

    def delete_pagamento(self, pagamento_id: str) -> bool:
        pagamento = self.get_pagamento(pagamento_id)
        if not pagamento:
            return False
        self.db.delete(pagamento)
        self.db.commit()
        return True
    
    def get_pagamentos_by_usuario(self, usuario_id: int) -> list[Pagamento]:
        """
        Retorna todos os pagamentos de um usuário ordenados por data (mais recente primeiro).
        """
        return (
            self.db.query(Pagamento)
            .filter(Pagamento.usuario_id == usuario_id)
            .order_by(Pagamento.data_pagamento.desc())
            .all()
        )
