from schemas.questoes import disciplina as schemas
from sqlalchemy.orm import Session
from models.questoes.disciplina import Disciplina
from repository.questoes.disciplina_repository import DisciplinaRepository
from fastapi import HTTPException
from starlette import status

class DisciplinaService:
    def __init__(self, db: Session):
        self.repo = DisciplinaRepository(db)
        
    def create_disciplina(self, disciplina: schemas.DisciplinaRequestDTO) -> schemas.DisciplinaResponseDTO:
        nome_normalizado = disciplina.nome.strip().lower().capitalize()
        if self.repo.get_by_name(nome_normalizado):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A disciplina '{nome_normalizado}' já existe."
            )
        db_disciplina = Disciplina(nome=nome_normalizado)
        saved_disciplina = self.repo.save(db_disciplina)
        return schemas.DisciplinaResponseDTO.model_validate(saved_disciplina)

    def get_disciplina(self, disciplina_id: int) -> schemas.DisciplinaResponseDTO:
        db_disciplina = self.repo.get_by_id(disciplina_id)
        if not db_disciplina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Disciplina não encontrada."
            )
        return schemas.DisciplinaResponseDTO.model_validate(db_disciplina)

    def get_all_disciplinas(self, skip: int = 0, limit: int = 100) -> list[schemas.DisciplinaResponseDTO]:
        disciplinas = self.repo.get_all(skip=skip, limit=limit)
        return [schemas.DisciplinaResponseDTO.model_validate(d) for d in disciplinas]

    def update_disciplina(self, disciplina_id: int, disciplina_dto: schemas.DisciplinaRequestDTO) -> schemas.DisciplinaResponseDTO:
        db_disciplina = self.repo.get_by_id(disciplina_id)
        if not db_disciplina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Disciplina não encontrada para atualização."
            )
        nome_normalizado = disciplina_dto.nome.strip().lower().capitalize()
        existing_disciplina = self.repo.get_by_name(nome_normalizado)
        if existing_disciplina and existing_disciplina.id != disciplina_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"O nome '{nome_normalizado}' já está em uso por outra disciplina."
            )
        db_disciplina.nome = nome_normalizado
        updated_disciplina = self.repo.save(db_disciplina)
        return schemas.DisciplinaResponseDTO.model_validate(updated_disciplina)

    def delete_disciplina(self, disciplina_id: int) -> None:
        db_disciplina = self.repo.get_by_id(disciplina_id)
        if not db_disciplina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Disciplina não encontrada para exclusão."
            )
        self.repo.delete(db_disciplina)
        return