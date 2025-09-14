from sqlalchemy.orm import Session
from models.usuarios.resolucao_questao_simulado import ResolucaoQuestaoSimulado
from repository.usuarios.resolucao_questao_simulado_repository import ResolucaoQuestaoSimuladoRepository
from schemas.usuarios.resolucao_questao_simulado import ResolucaoQuestaoSimuladoRequestDTO, ResolucaoQuestaoSimuladoResponseDTO

class ResolucaoQuestaoSimuladoService:
    def __init__(self, db: Session):
        self.repo = ResolucaoQuestaoSimuladoRepository(db)

    def create_resolucao(self, resolucao: ResolucaoQuestaoSimuladoRequestDTO) -> dict:
        db_resolucao = ResolucaoQuestaoSimulado(**resolucao.model_dump())
        db_resolucao = self.repo.create_resolucao(db_resolucao)
        return ResolucaoQuestaoSimuladoResponseDTO.model_validate(db_resolucao).model_dump(mode="json")

    def get_resolucao(self, resolucao_id: int) -> dict | None:
        db_resolucao = self.repo.get_resolucao(resolucao_id)
        if db_resolucao:
            return ResolucaoQuestaoSimuladoResponseDTO.model_validate(db_resolucao).model_dump(mode="json")
        return None

    def get_all_resolucoes(self, skip: int, limit: int) -> list[dict]:
        resolucoes = self.repo.get_all_resolucoes(skip=skip, limit=limit)
        return [ResolucaoQuestaoSimuladoResponseDTO.model_validate(r).model_dump(mode="json") for r in resolucoes]

    def update_resolucao(self, resolucao_id: int, resolucao: ResolucaoQuestaoSimuladoRequestDTO) -> dict | None:
        novos_dados = resolucao.model_dump()
        db_resolucao = self.repo.update_resolucao(resolucao_id, novos_dados)
        if db_resolucao:
            return ResolucaoQuestaoSimuladoResponseDTO.model_validate(db_resolucao).model_dump(mode="json")
        return None

    def delete_resolucao(self, resolucao_id: int) -> bool:
        return self.repo.delete_resolucao(resolucao_id)
