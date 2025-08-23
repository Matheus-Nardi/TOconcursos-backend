from schemas.questoes import instituicao as schemas
from sqlalchemy.orm import Session
from models.questoes.instituicao import Instituicao
from repository.questoes.instituicao_repository import InstituicaoRepository

class InstituicaoService:
    def __init__(self, db: Session):
        self.repo = InstituicaoRepository(db)
        
    def create_instituicao(self, instituicao: schemas.InstituicaoRequestDTO) -> schemas.InstituicaoResponseDTO:
        nome_normalizado = instituicao.nome.strip().lower().capitalize()
        
        # Criar uma execption personalizada se a instituicao já existir
        if self.repo.get_instituicao_by_name(nome_normalizado):
            raise ValueError(
                f"Instituicao with name '{nome_normalizado}' already exists."
            )
        
        instituicao_normalizada = schemas.InstituicaoRequestDTO(nome=nome_normalizado)
        db_instituicao = self.repo.create_instituicao(instituicao_normalizada)
        
        return schemas.InstituicaoResponseDTO.model_validate(db_instituicao)

    def get_instituicao(self, instituicao_id: int) -> schemas.InstituicaoResponseDTO:
        db_instituicao = self.repo.get_instituicao(instituicao_id)
        if db_instituicao:
            return schemas.InstituicaoResponseDTO.model_validate(db_instituicao)
        return None

    def get_all_instituicaos(self, skip, limit) -> list[schemas.InstituicaoResponseDTO]:
        instituicaos = self.repo.get_all_instituicaos(skip=skip, limit=limit)
        return [schemas.InstituicaoResponseDTO.model_validate(d) for d in instituicaos]

    def update_instituicao(self, instituicao_id: int, instituicao: schemas.InstituicaoRequestDTO) -> schemas.InstituicaoResponseDTO:
        nome_normalizado = instituicao.nome.strip().lower().capitalize()
        instituicao_normalizada = schemas.InstituicaoRequestDTO(nome=nome_normalizado)
        
        db_instituicao = self.repo.update_instituicao(instituicao_id, instituicao_normalizada)
        if db_instituicao:
            return schemas.InstituicaoResponseDTO.model_validate(db_instituicao)
        return None

    def delete_instituicao(self, instituicao_id: int) -> bool:
        return self.repo.delete_instituicao(instituicao_id)