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
        db_resolucao = self.repo.create_resolucao(db_resolucao)
        
        # Monta o DTO manualmente para calcular ja_respondeu corretamente
        from schemas.questoes.questao import QuestaoSimplificadaResponseDTO
        questao_simplificada = QuestaoSimplificadaResponseDTO(
            id=db_questao.id,
            enunciado=db_questao.enunciado,
            ja_respondeu=True  # Se há uma resolução, a questão já foi respondida por esse usuário
        )
        
        return ResolucaoQuestaoResponseDTO(
            id=db_resolucao.id,
            is_certa=db_resolucao.is_certa,
            questao=questao_simplificada,
            data_resolucao=db_resolucao.data_resolucao
        )


    def get_all_resolucoes(self, skip: int, limit: int, user_id: int) -> list[ResolucaoQuestaoResponseDTO]:
        resolucoes = self.repo.get_all_resolucoes(skip=skip, limit=limit, user_id=user_id)
        
        from schemas.questoes.questao import QuestaoSimplificadaResponseDTO
        result = []
        for r in resolucoes:
            questao_simplificada = QuestaoSimplificadaResponseDTO(
                id=r.questao.id,
                enunciado=r.questao.enunciado,
                ja_respondeu=True  # Se há uma resolução, a questão já foi respondida por esse usuário
            )
            result.append(ResolucaoQuestaoResponseDTO(
                id=r.id,
                is_certa=r.is_certa,
                questao=questao_simplificada,
                data_resolucao=r.data_resolucao
            ))
        
        return result
