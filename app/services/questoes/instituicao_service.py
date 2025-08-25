from schemas.questoes import instituicao as schemas
from sqlalchemy.orm import Session
from models.questoes.instituicao import Instituicao
from repository.questoes.instituicao_repository import InstituicaoRepository
from fastapi import HTTPException
from starlette import status

class InstituicaoService:
    def __init__(self, db: Session):
        self.repo = InstituicaoRepository(db)
        
    def create_instituicao(self, instituicao_dto: schemas.InstituicaoRequestDTO) -> schemas.InstituicaoResponseDTO:
        nome_normalizado = instituicao_dto.nome.strip().lower().capitalize()
        if self.repo.get_by_name(nome_normalizado):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A instituição '{nome_normalizado}' já existe."
            )
        db_instituicao = Instituicao(nome=nome_normalizado)
        saved_instituicao = self.repo.save(db_instituicao)
        return schemas.InstituicaoResponseDTO.model_validate(saved_instituicao)

    def get_instituicao(self, instituicao_id: int) -> schemas.InstituicaoResponseDTO:
        db_instituicao = self.repo.get_by_id(instituicao_id)
        if not db_instituicao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Instituição não encontrada."
            )
        return schemas.InstituicaoResponseDTO.model_validate(db_instituicao)

    def get_all_instituicoes(self, skip: int = 0, limit: int = 100) -> list[schemas.InstituicaoResponseDTO]:
        instituicoes = self.repo.get_all(skip=skip, limit=limit)
        return [schemas.InstituicaoResponseDTO.model_validate(d) for d in instituicoes]

    def update_instituicao(self, instituicao_id: int, instituicao_dto: schemas.InstituicaoRequestDTO) -> schemas.InstituicaoResponseDTO:
        db_instituicao = self.repo.get_by_id(instituicao_id)
        if not db_instituicao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Instituição não encontrada para atualização."
            )
        nome_normalizado = instituicao_dto.nome.strip().lower().capitalize()
        existing_instituicao = self.repo.get_by_name(nome_normalizado)
        if existing_instituicao and existing_instituicao.id != instituicao_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"O nome '{nome_normalizado}' já está em uso por outra instituição."
            )
        db_instituicao.nome = nome_normalizado
        updated_instituicao = self.repo.save(db_instituicao)
        return schemas.InstituicaoResponseDTO.model_validate(updated_instituicao)

    def delete_instituicao(self, instituicao_id: int) -> None:
        db_instituicao = self.repo.get_by_id(instituicao_id)
        if not db_instituicao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Instituição não encontrada para exclusão."
            )
        
        self.repo.delete(db_instituicao)
        
        return