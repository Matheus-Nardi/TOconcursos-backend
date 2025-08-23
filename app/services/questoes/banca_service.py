from schemas.questoes import banca as schemas
from sqlalchemy.orm import Session
from models.questoes.banca import Banca
from repository.questoes.banca_repository import BancaRepository

class BancaService:
    def __init__(self, db: Session):
        self.repo = BancaRepository(db)
        
    def create_banca(self, banca: schemas.BancaRequestDTO) -> schemas.BancaResponseDTO:
        nome_normalizado = banca.nome.strip().lower().capitalize()
        
        # Criar uma execption personalizada se a banca já existir
        if self.repo.get_banca_by_name(nome_normalizado):
            raise ValueError(
                f"Banca with name '{nome_normalizado}' already exists."
            )
        
        banca_normalizada = schemas.BancaRequestDTO(nome=nome_normalizado)
        db_banca = self.repo.create_banca(banca_normalizada)
        
        return schemas.BancaResponseDTO.model_validate(db_banca)

    def get_banca(self, banca_id: int) -> schemas.BancaResponseDTO:
        db_banca = self.repo.get_banca(banca_id)
        if db_banca:
            return schemas.BancaResponseDTO.model_validate(db_banca)
        return None

    def get_all_bancas(self, skip, limit) -> list[schemas.BancaResponseDTO]:
        bancas = self.repo.get_all_bancas(skip=skip, limit=limit)
        return [schemas.BancaResponseDTO.model_validate(d) for d in bancas]

    def update_banca(self, banca_id: int, banca: schemas.BancaRequestDTO) -> schemas.BancaResponseDTO:
        nome_normalizado = banca.nome.strip().lower().capitalize()
        banca_normalizada = schemas.BancaRequestDTO(nome=nome_normalizado)
        
        db_banca = self.repo.update_banca(banca_id, banca_normalizada)
        if db_banca:
            return schemas.BancaResponseDTO.model_validate(db_banca)
        return None

    def delete_banca(self, banca_id: int) -> bool:
        return self.repo.delete_banca(banca_id)