from sqlalchemy.orm import Session
from models.usuarios.resolucao_questao_simulado import ResolucaoQuestaoSimulado

class ResolucaoQuestaoSimuladoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_resolucao(self, resolucao: ResolucaoQuestaoSimulado) -> ResolucaoQuestaoSimulado:
        self.db.add(resolucao)
        self.db.commit()
        self.db.refresh(resolucao)
        return resolucao

    def get_resolucao(self, resolucao_id: int) -> ResolucaoQuestaoSimulado | None:
        return self.db.query(ResolucaoQuestaoSimulado).filter(ResolucaoQuestaoSimulado.id == resolucao_id).first()

    def get_all_resolucoes(self, skip: int = 0, limit: int = 10) -> list[ResolucaoQuestaoSimulado]:
        return self.db.query(ResolucaoQuestaoSimulado).offset(skip).limit(limit).all()

    def update_resolucao(self, resolucao_id: int, novos_dados: dict) -> ResolucaoQuestaoSimulado | None:
        resolucao = self.get_resolucao(resolucao_id)
        if not resolucao:
            return None
        for campo, valor in novos_dados.items():
            setattr(resolucao, campo, valor)
        self.db.commit()
        self.db.refresh(resolucao)
        return resolucao

    def delete_resolucao(self, resolucao_id: int) -> bool:
        resolucao = self.get_resolucao(resolucao_id)
        if not resolucao:
            return False
        self.db.delete(resolucao)
        self.db.commit()
        return True
