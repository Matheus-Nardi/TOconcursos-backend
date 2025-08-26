from schemas.questoes import disciplina as schemas
from sqlalchemy.orm import Session
from models.questoes.disciplina import Disciplina
from repository.questoes.disciplina_repository import DisciplinaRepository
from fastapi import HTTPException

class DisciplinaService:
    def __init__(self, db: Session):
        self.repo = DisciplinaRepository(db)
        
    def create_disciplina(self, disciplina: schemas.DisciplinaRequestDTO) -> schemas.DisciplinaResponseDTO:
        nome_normalizado = disciplina.nome.strip().lower().capitalize()
        
        # Criar uma execption personalizada se a disciplina já existir
        if self.repo.get_disciplina_by_name(nome_normalizado):
            raise ValueError(
                f"Disciplina with name '{nome_normalizado}' already exists."
            )
        
        disciplina_normalizada = schemas.DisciplinaRequestDTO(nome=nome_normalizado)
        db_disciplina = self.repo.create_disciplina(disciplina_normalizada)
        
        return schemas.DisciplinaResponseDTO.model_validate(db_disciplina)

    def get_disciplina(self, disciplina_id: int) -> schemas.DisciplinaResponseDTO:
        db_disciplina = self.repo.get_disciplina(disciplina_id)
        if db_disciplina:
            return schemas.DisciplinaResponseDTO.model_validate(db_disciplina)
        return None

    def get_all_disciplinas(self) -> list[schemas.DisciplinaResponseDTO]:
        disciplinas = self.repo.get_all_disciplinas()
        return [schemas.DisciplinaResponseDTO.model_validate(d) for d in disciplinas]

    def update_disciplina(self, disciplina_id: int, disciplina: schemas.DisciplinaRequestDTO) -> schemas.DisciplinaResponseDTO:
        nome_normalizado = disciplina.nome.strip().lower().capitalize()
        disciplina_normalizada = schemas.DisciplinaRequestDTO(nome=nome_normalizado)
        
        db_disciplina = self.repo.update_disciplina(disciplina_id, disciplina_normalizada)
        if db_disciplina:
            return schemas.DisciplinaResponseDTO.model_validate(db_disciplina)
        return None

    def delete_disciplina(self, disciplina_id: int) -> bool:
        return self.repo.delete_disciplina(disciplina_id)