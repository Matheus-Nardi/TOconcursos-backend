from sqlalchemy.orm import Session
from models.usuarios.resolucao_questao import ResolucaoQuestao
from repository.usuarios.resolucao_questao_repository import ResolucaoQuestaoRepository
from schemas.usuarios.resolucao_questao import ResolucaoQuestaoRequestDTO, ResolucaoQuestaoResponseDTO
from datetime import datetime
from core.exceptions.exception import NotFoundException
from repository.usuarios.usuario_repository import UsuarioRepository
from repository.questoes.questao_repository import QuestaoRepository


class ResolucaoQuestaoService:
    def __init__(self, db: Session):
        self.repo = ResolucaoQuestaoRepository(db)
        self.usuario_repo = UsuarioRepository(db)
        self.questao_repo = QuestaoRepository(db)

    def create_resolucao(self, resolucao: ResolucaoQuestaoRequestDTO, user_id: int) -> ResolucaoQuestaoResponseDTO:
        db_user = self.usuario_repo.get_usuario(user_id)
        if not db_user:
            raise NotFoundException("Usuário não encontrado")

        db_questao = self.questao_repo.get_questao(resolucao.questao_id)
        if not db_questao:
            raise NotFoundException("Questão não encontrada")
        
        db_resolucao = ResolucaoQuestao(
            is_certa=resolucao.is_certa,
            questao=db_questao,
            data_resolucao=datetime.utcnow(),
            usuario=db_user
        )
        self.questao_repo.update_already_answered(db_questao.id, True)
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
