from sqlalchemy.orm import Session
from models.usuarios.resolucao_questao_simulado import ResolucaoQuestaoSimulado
from repository.usuarios.resolucao_questao_simulado_repository import ResolucaoQuestaoSimuladoRepository
from schemas.usuarios.resolucao_questao_simulado import ResolucaoQuestaoSimuladoRequestDTO, ResolucaoQuestaoSimuladoResponseDTO

class ResolucaoQuestaoSimuladoService:
    def __init__(self, db: Session):
        self.repo = ResolucaoQuestaoSimuladoRepository(db)

    def create_resolucao(self, resolucao: ResolucaoQuestaoSimuladoRequestDTO) -> ResolucaoQuestaoSimuladoResponseDTO:
        db_resolucao = ResolucaoQuestaoSimulado(**resolucao.model_dump())
        db_resolucao = self.repo.create_resolucao(db_resolucao)
        return ResolucaoQuestaoSimuladoResponseDTO.model_validate(db_resolucao)

    def get_resolucao(self, resolucao_id: int) -> ResolucaoQuestaoSimuladoResponseDTO | None:
        db_resolucao = self.repo.get_resolucao(resolucao_id)
        if db_resolucao:
            return ResolucaoQuestaoSimuladoResponseDTO.model_validate(db_resolucao)
        return None

    def get_all_resolucoes(self, skip: int, limit: int) -> list[ResolucaoQuestaoSimuladoResponseDTO]:
        resolucoes = self.repo.get_all_resolucoes(skip=skip, limit=limit)
        return [ResolucaoQuestaoSimuladoResponseDTO.model_validate(r) for r in resolucoes]

    def update_resolucao(self, resolucao_id: int, resolucao: ResolucaoQuestaoSimuladoRequestDTO) -> ResolucaoQuestaoSimuladoResponseDTO | None:
        novos_dados = resolucao.model_dump()
        db_resolucao = self.repo.update_resolucao(resolucao_id, novos_dados)
        if db_resolucao:
            return ResolucaoQuestaoSimuladoResponseDTO.model_validate(db_resolucao)
        return None

    def delete_resolucao(self, resolucao_id: int) -> bool:
        return self.repo.delete_resolucao(resolucao_id)
