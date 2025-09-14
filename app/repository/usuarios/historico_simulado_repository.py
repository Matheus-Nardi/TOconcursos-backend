from sqlalchemy.orm import Session
from models.usuarios.historico_simulado import HistoricoSimulado

class HistoricoSimuladoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_historico(self, historico: HistoricoSimulado) -> HistoricoSimulado:
        self.db.add(historico)
        self.db.commit()
        self.db.refresh(historico)
        return historico

    def get_historico(self, historico_id: int) -> HistoricoSimulado | None:
        return self.db.query(HistoricoSimulado).filter(HistoricoSimulado.id == historico_id).first()

    def get_all_historicos(self, skip: int = 0, limit: int = 10) -> list[HistoricoSimulado]:
        return self.db.query(HistoricoSimulado).offset(skip).limit(limit).all()

    def update_historico(self, historico_id: int, novos_dados: dict) -> HistoricoSimulado | None:
        historico = self.get_historico(historico_id)
        if not historico:
            return None
        for campo, valor in novos_dados.items():
            setattr(historico, campo, valor)
        self.db.commit()
        self.db.refresh(historico)
        return historico

    def delete_historico(self, historico_id: int) -> bool:
        historico = self.get_historico(historico_id)
        if not historico:
            return False
        self.db.delete(historico)
        self.db.commit()
        return True
