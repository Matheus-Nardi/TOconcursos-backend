from sqlalchemy.orm import Session
from repository.usuarios.resolucao_questao_repository import ResolucaoQuestaoRepository
from datetime import datetime
from schemas.usuarios.objetivo import ObjetivoResponseDTO
from repository.usuarios.resolucao_questao_repository import ResolucaoQuestaoRepository

class GraficosService:
    def __init__(self, db: Session):
        self.repo = ResolucaoQuestaoRepository(db)

    def get_quantidade_questoes_por_dia(self, usuario_id: int):
        return self.repo.get_quantidade_questoes_por_dia(usuario_id)

    def get_quantidade_certo_errado_por_dia(self, usuario_id: int):
        return self.repo.get_quantidade_certo_errado_por_dia(usuario_id)