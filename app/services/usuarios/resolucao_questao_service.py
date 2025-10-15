from sqlalchemy.orm import Session
from models.usuarios.resolucao_questao import ResolucaoQuestao
from repository.usuarios.resolucao_questao_repository import ResolucaoQuestaoRepository
from schemas.usuarios.resolucao_questao import ResolucaoQuestaoRequestDTO, ResolucaoQuestaoResponseDTO
from datetime import datetime
from core.exceptions.exception import NotFoundException

class ResolucaoQuestaoService:
    def __init__(self, db: Session):
        self.repo = ResolucaoQuestaoRepository(db)

    def create_resolucao(self, resolucao: ResolucaoQuestaoRequestDTO) -> ResolucaoQuestaoResponseDTO:
        db_resolucao = ResolucaoQuestao(
            is_certa=resolucao.is_certa,
            historico_id=resolucao.historico_id,
            questao_id=resolucao.questao_id,
            data_resolucao=resolucao.data_resolucao or datetime.utcnow()
        )
        db_resolucao = self.repo.create_resolucao(db_resolucao)
        return ResolucaoQuestaoResponseDTO.model_validate(db_resolucao)

    def get_resolucao(self, resolucao_id: int) -> ResolucaoQuestaoResponseDTO:
        db_resolucao = self.repo.get_resolucao(resolucao_id)
        if not db_resolucao:
            raise NotFoundException("Resolução de questão não encontrada")
        return ResolucaoQuestaoResponseDTO.model_validate(db_resolucao)

    def get_all_resolucoes(self, skip: int, limit: int) -> list[ResolucaoQuestaoResponseDTO]:
        resolucoes = self.repo.get_all_resolucoes(skip=skip, limit=limit)
        return [ResolucaoQuestaoResponseDTO.model_validate(r) for r in resolucoes]

    def update_resolucao(self, resolucao_id: int, resolucao: ResolucaoQuestaoRequestDTO) -> ResolucaoQuestaoResponseDTO:
        novos_dados = resolucao.model_dump()
        db_resolucao = self.repo.update_resolucao(resolucao_id, novos_dados)
        if not db_resolucao:
            raise NotFoundException("Resolução de questão não encontrada")
        return ResolucaoQuestaoResponseDTO.model_validate(db_resolucao)

    def delete_resolucao(self, resolucao_id: int) -> bool:
        return self.repo.delete_resolucao(resolucao_id)
