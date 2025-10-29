from schemas.planos import plano as schemas
from sqlalchemy.orm import Session
from repository.planos.plano_repository import PlanoRepository
from core.exceptions.exception import NotFoundException

class PlanoService:
    def __init__(self, db: Session):
        self.repo = PlanoRepository(db)
   
    def get_plano(self, plano_id: int) -> schemas.PlanoResponseDTO:
        db_plano = self.repo.get_by_id(plano_id)
        
        if not db_plano:
            raise NotFoundException("Plano não encontrada")
            
        return schemas.PlanoResponseDTO.model_validate(db_plano)

    def get_all_planos(self, skip: int = 0, limit: int = 100) -> list[schemas.PlanoResponseDTO]:
        planos = self.repo.get_all(skip=skip, limit=limit)
        return [schemas.PlanoResponseDTO.model_validate(b) for b in planos]

