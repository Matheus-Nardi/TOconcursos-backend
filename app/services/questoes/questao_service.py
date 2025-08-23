from schemas.questoes import questao as schemas
from sqlalchemy.orm import Session
from models.questoes.questao import Questao
from repository.questoes.questoes_repository import QuestaoRepository
from fastapi import HTTPException

class QuestaoService:
    def __init__(self, db: Session):
        self.repo = QuestaoRepository(db)

    # def create_questao(self, questao: schemas.QuestaoRequestDTO) -> schemas.QuestaoResponseDTO:
    #     nome_normalizado = questao.nome.strip().lower().capitalize()
        
    #     # Criar uma execption personalizada se a questao já existir
    #     if self.repo.get_questao_by_name(nome_normalizado):
    #         raise ValueError(
    #             f"questao with name '{nome_normalizado}' already exists."
    #         )
        
    #     questao_normalizada = schemas.QuestaoRequestDTO(nome=nome_normalizado)
    #     db_questao = self.repo.create_Questao(questao_normalizada)

    #     return schemas.QuestaoResponseDTO.model_validate(db_questao)

    def get_questao(self, questao_id: int) -> schemas.QuestaoResponseDTO:
        db_questao = self.repo.get_questao(questao_id)
        if db_questao:
            return schemas.QuestaoResponseDTO.model_validate(db_questao)
        return None
    
    def get_all_questaos(self) -> list[schemas.QuestaoResponseDTO]:
        db_questaos = self.repo.get_all_questoes()
        return [schemas.QuestaoResponseDTO.model_validate(d) for d in db_questaos]

    def update_questao(self, questao_id: int, questao: schemas.QuestaoRequestDTO) -> schemas.QuestaoResponseDTO:
        nome_normalizado = questao.nome.strip().lower().capitalize()
        questao_normalizada = schemas.QuestaoRequestDTO(nome=nome_normalizado)

        db_questao = self.repo.update_questao(questao_id, questao_normalizada)
        if db_questao:
            return schemas.QuestaoResponseDTO.model_validate(db_questao)
        return None

    def delete_questao(self, questao_id: int) -> bool:
        return self.repo.delete_questao(questao_id)
