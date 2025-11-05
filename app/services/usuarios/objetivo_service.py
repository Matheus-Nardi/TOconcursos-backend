from sqlalchemy.orm import Session
from repository.usuarios.resolucao_questao_repository import ResolucaoQuestaoRepository
from datetime import datetime
from schemas.usuarios.objetivo import ObjetivoResponseDTO
from repository.usuarios.objetivo_repository import ObjetivoRepository

class ObjetivoService:
    def __init__(self, db: Session):
        self.repo = ObjetivoRepository(db)

    def get_all_objetivos(self, skip: int, limit: int) -> list[ObjetivoResponseDTO]:
        objetivos = self.repo.get_all_objetivos(skip=skip, limit=limit)
        return [ObjetivoResponseDTO.model_validate(o) for o in objetivos]
