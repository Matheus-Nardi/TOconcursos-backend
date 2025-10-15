from sqlalchemy.orm import Session
from models.usuarios.resolucao_questao import ResolucaoQuestao

class ResolucaoQuestaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_resolucao(self, resolucao: ResolucaoQuestao) -> ResolucaoQuestao:
        self.db.add(resolucao)
        self.db.commit()
        self.db.refresh(resolucao)
        return resolucao


    def get_all_resolucoes(self, skip: int = 0, limit: int = 10, user_id: int = 0) -> list[ResolucaoQuestao]:
        return self.db.query(ResolucaoQuestao).filter(ResolucaoQuestao.usuario_id == user_id).offset(skip).limit(limit).all()
