from schemas.questoes import banca as schemas
from sqlalchemy.orm import Session
from models.questoes.banca import Banca
from repository.questoes.banca_repository import BancaRepository
from fastapi import HTTPException
from starlette import status

class BancaService:
    def __init__(self, db: Session):
        self.repo = BancaRepository(db)
        
    def create_banca(self, banca_dto: schemas.BancaRequestDTO) -> schemas.BancaResponseDTO:
        nome_normalizado = banca_dto.nome.strip().lower().capitalize()
        
        if self.repo.get_by_name(nome_normalizado):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A banca '{nome_normalizado}' já existe."
            )
        
        db_banca = Banca(nome=nome_normalizado)
        saved_banca = self.repo.save(db_banca)
        
        return schemas.BancaResponseDTO.model_validate(saved_banca)

    def get_banca(self, banca_id: int) -> schemas.BancaResponseDTO:
        db_banca = self.repo.get_by_id(banca_id)
        
        if not db_banca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Banca não encontrada."
            )
            
        return schemas.BancaResponseDTO.model_validate(db_banca)

    def get_all_bancas(self, skip: int = 0, limit: int = 100) -> list[schemas.BancaResponseDTO]:
        bancas = self.repo.get_all(skip=skip, limit=limit)
        return [schemas.BancaResponseDTO.model_validate(b) for b in bancas]

    def update_banca(self, banca_id: int, banca_dto: schemas.BancaRequestDTO) -> schemas.BancaResponseDTO:
        db_banca = self.repo.get_by_id(banca_id)
        if not db_banca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Banca não encontrada para atualização."
            )
        
        nome_normalizado = banca_dto.nome.strip().lower().capitalize()

        existing_banca = self.repo.get_by_name(nome_normalizado)
        if existing_banca and existing_banca.id != banca_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"O nome '{nome_normalizado}' já está em uso por outra banca."
            )

        db_banca.nome = nome_normalizado
        updated_banca = self.repo.save(db_banca)
        
        return schemas.BancaResponseDTO.model_validate(updated_banca)

    def delete_banca(self, banca_id: int) -> None:
        db_banca = self.repo.get_by_id(banca_id)
        if not db_banca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Banca não encontrada para exclusão."
            )
        
        self.repo.delete(db_banca)
        
        return