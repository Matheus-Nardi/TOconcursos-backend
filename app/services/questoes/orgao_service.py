from schemas.questoes import orgao as schemas
from sqlalchemy.orm import Session
from models.questoes.orgao import Orgao
from repository.questoes.orgao_repository import OrgaoRepository
from fastapi import HTTPException
from starlette import status

class OrgaoService:
    def __init__(self, db: Session):
        self.repo = OrgaoRepository(db)
        
    def create_orgao(self, orgao_dto: schemas.OrgaoRequestDTO) -> schemas.OrgaoResponseDTO:
        nome_normalizado = orgao_dto.nome.strip().lower().capitalize()
        if self.repo.get_by_name(nome_normalizado):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"O órgão '{nome_normalizado}' já existe."
            )
        db_orgao = Orgao(nome=nome_normalizado)
        saved_orgao = self.repo.save(db_orgao)
        return schemas.OrgaoResponseDTO.model_validate(saved_orgao)

    def get_orgao(self, orgao_id: int) -> schemas.OrgaoResponseDTO:
        db_orgao = self.repo.get_by_id(orgao_id)
        if not db_orgao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Órgão não encontrado."
            )
        return schemas.OrgaoResponseDTO.model_validate(db_orgao)

    def get_all_orgaos(self, skip: int = 0, limit: int = 100) -> list[schemas.OrgaoResponseDTO]:
        orgaos = self.repo.get_all(skip=skip, limit=limit)
        return [schemas.OrgaoResponseDTO.model_validate(d) for d in orgaos]

    def update_orgao(self, orgao_id: int, orgao_dto: schemas.OrgaoRequestDTO) -> schemas.OrgaoResponseDTO:
        db_orgao = self.repo.get_by_id(orgao_id)
        if not db_orgao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Órgão não encontrado para atualização."
            )
        nome_normalizado = orgao_dto.nome.strip().lower().capitalize()
        existing_orgao = self.repo.get_by_name(nome_normalizado)
        if existing_orgao and existing_orgao.id != orgao_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"O nome '{nome_normalizado}' já está em uso por outro órgão."
            )
        db_orgao.nome = nome_normalizado
        updated_orgao = self.repo.save(db_orgao)
        return schemas.OrgaoResponseDTO.model_validate(updated_orgao)

    def delete_orgao(self, orgao_id: int) -> None:
        db_orgao = self.repo.get_by_id(orgao_id)
        if not db_orgao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Órgão não encontrado para exclusão."
            )
        self.repo.delete(db_orgao)
        return