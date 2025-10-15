from schemas.questoes import instituicao as schemas
from sqlalchemy.orm import Session
from models.questoes.instituicao import Instituicao
from repository.questoes.instituicao_repository import InstituicaoRepository
from core.exceptions.exception import NotFoundException, ConflictException

class InstituicaoService:
    def __init__(self, db: Session):
        self.repo = InstituicaoRepository(db)
        
    def create_instituicao(self, instituicao_dto: schemas.InstituicaoRequestDTO) -> schemas.InstituicaoResponseDTO:
        label_normalizado = instituicao_dto.label.strip().lower().capitalize()
        if self.repo.get_by_name(label_normalizado):
            raise ConflictException(f"A instituição '{label_normalizado}' já existe")
        db_instituicao = Instituicao(label=label_normalizado)
        saved_instituicao = self.repo.save(db_instituicao)
        return schemas.InstituicaoResponseDTO.model_validate(saved_instituicao)

    def get_instituicao(self, instituicao_id: int) -> schemas.InstituicaoResponseDTO:
        db_instituicao = self.repo.get_by_id(instituicao_id)
        if not db_instituicao:
            raise NotFoundException("Instituição não encontrada")
        return schemas.InstituicaoResponseDTO.model_validate(db_instituicao)

    def get_all_instituicoes(self, skip: int = 0, limit: int = 100) -> list[schemas.InstituicaoResponseDTO]:
        instituicoes = self.repo.get_all(skip=skip, limit=limit)
        return [schemas.InstituicaoResponseDTO.model_validate(d) for d in instituicoes]

    def update_instituicao(self, instituicao_id: int, instituicao_dto: schemas.InstituicaoRequestDTO) -> schemas.InstituicaoResponseDTO:
        db_instituicao = self.repo.get_by_id(instituicao_id)
        if not db_instituicao:
            raise NotFoundException("Instituição não encontrada")
        label_normalizado = instituicao_dto.label.strip().lower().capitalize()
        existing_instituicao = self.repo.get_by_name(label_normalizado)
        if existing_instituicao and existing_instituicao.id != instituicao_id:
            raise ConflictException(f"O label '{label_normalizado}' já está em uso por outra instituição")
        db_instituicao.label = label_normalizado
        updated_instituicao = self.repo.save(db_instituicao)
        return schemas.InstituicaoResponseDTO.model_validate(updated_instituicao)

    def delete_instituicao(self, instituicao_id: int) -> None:
        db_instituicao = self.repo.get_by_id(instituicao_id)
        if not db_instituicao:
            raise NotFoundException("Instituição não encontrada")
        
        self.repo.delete(db_instituicao)
        
        return