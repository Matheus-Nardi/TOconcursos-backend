from schemas.questoes import questao as schemas
from sqlalchemy.orm import Session
from models.questoes.questao import Questao
from repository.questoes.questao_repository import QuestaoRepository
from repository.questoes.disciplina_repository import DisciplinaRepository
from repository.questoes.orgao_repository import OrgaoRepository
from repository.questoes.instituicao_repository import InstituicaoRepository
from repository.questoes.banca_repository import BancaRepository

from models.questoes import alternativa as models
class QuestaoService:
    def __init__(self, db: Session):
        self.repo = QuestaoRepository(db)
        self.disciplina_repo = DisciplinaRepository(db)
        self.orgao_repo = OrgaoRepository(db)
        self.instituicao_repo = InstituicaoRepository(db)
        self.banca_repo = BancaRepository(db)

    def create_questao(self, questao: schemas.QuestaoRequestDTO) -> schemas.QuestaoResponseDTO:
        db_disciplina = self.disciplina_repo.get_by_id(questao.id_disciplina)
        if not db_disciplina:
            raise ValueError(f"Disciplina with id {questao.id_disciplina} not found.")

        db_orgao = self.orgao_repo.get_by_id(questao.id_orgao)
        if not db_orgao:
            raise ValueError(f"Orgao with id {questao.id_orgao} not found.")

        db_instituicao = self.instituicao_repo.get_by_id(questao.id_instituicao)
        if not db_instituicao:
            raise ValueError(f"Instituicao with id {questao.id_instituicao} not found.")

        db_banca = self.banca_repo.get_by_id(questao.id_banca)
        if not db_banca:
            raise ValueError(f"Banca with id {questao.id_banca} not found.")


        db_alternativas = [
            models.Alternativa(descricao=alt.descricao, is_correta=alt.is_correta)
            for alt in questao.alternativas
        ]
        db_questao = Questao(
            enunciado = questao.enunciado,
            disciplina = db_disciplina,
            orgao = db_orgao,
            instituicao = db_instituicao,
            banca = db_banca,
            alternativas = db_alternativas
            
        )

        db_questao = self.repo.create_questao(db_questao)
        

        return schemas.QuestaoResponseDTO.model_validate(db_questao)

    def get_questao(self, questao_id: int) -> schemas.QuestaoResponseDTO:
        db_questao = self.repo.get_questao(questao_id)
        if db_questao:
            return schemas.QuestaoResponseDTO.model_validate(db_questao)
        return None

    def get_all_questaos(self, skip, limit) -> list[schemas.QuestaoResponseDTO]:
        questaos = self.repo.get_all_questaos(skip=skip, limit=limit)
        return [schemas.QuestaoResponseDTO.model_validate(d) for d in questaos]


    # Futuramente um soft delete
    def delete_questao(self, questao_id: int) -> bool:
        return self.repo.delete_questao(questao_id)