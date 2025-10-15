from schemas.questoes import disciplina as schemas
from sqlalchemy.orm import Session
from models.questoes.disciplina import Disciplina
from repository.questoes.disciplina_repository import DisciplinaRepository
from core.exceptions.exception import NotFoundException, ConflictException

class DisciplinaService:
    def __init__(self, db: Session):
        self.repo = DisciplinaRepository(db)
        
    def create_disciplina(self, disciplina: schemas.DisciplinaRequestDTO) -> schemas.DisciplinaResponseDTO:
        label_normalizado = disciplina.label.strip().lower().capitalize()
        if self.repo.get_by_name(label_normalizado):
            raise ConflictException(f"A disciplina '{label_normalizado}' já existe")
        db_disciplina = Disciplina(label=label_normalizado)
        saved_disciplina = self.repo.save(db_disciplina)
        return schemas.DisciplinaResponseDTO.model_validate(saved_disciplina)

    def get_disciplina(self, disciplina_id: int) -> schemas.DisciplinaResponseDTO:
        db_disciplina = self.repo.get_by_id(disciplina_id)
        if not db_disciplina:
            raise NotFoundException("Disciplina não encontrada")
        return schemas.DisciplinaResponseDTO.model_validate(db_disciplina)

    def get_all_disciplinas(self, skip: int = 0, limit: int = 100) -> list[schemas.DisciplinaResponseDTO]:
        disciplinas = self.repo.get_all(skip=skip, limit=limit)
        return [schemas.DisciplinaResponseDTO.model_validate(d) for d in disciplinas]

    def update_disciplina(self, disciplina_id: int, disciplina_dto: schemas.DisciplinaRequestDTO) -> schemas.DisciplinaResponseDTO:
        db_disciplina = self.repo.get_by_id(disciplina_id)
        if not db_disciplina:
            raise NotFoundException("Disciplina não encontrada")
        label_normalizado = disciplina_dto.label.strip().lower().capitalize()
        existing_disciplina = self.repo.get_by_name(label_normalizado)
        if existing_disciplina and existing_disciplina.id != disciplina_id:
            raise ConflictException(f"O label '{label_normalizado}' já está em uso por outra disciplina")
        db_disciplina.label = label_normalizado
        updated_disciplina = self.repo.save(db_disciplina)
        return schemas.DisciplinaResponseDTO.model_validate(updated_disciplina)

    def delete_disciplina(self, disciplina_id: int) -> None:
        db_disciplina = self.repo.get_by_id(disciplina_id)
        if not db_disciplina:
            raise NotFoundException("Disciplina não encontrada")
        self.repo.delete(db_disciplina)
        return