from schemas.questoes import orgao as schemas
from sqlalchemy.orm import Session
from models.questoes.orgao import Orgao
from repository.questoes.orgao_repository import OrgaoRepository

class OrgaoService:
    def __init__(self, db: Session):
        self.repo = OrgaoRepository(db)
        
    def create_orgao(self, orgao: schemas.OrgaoRequestDTO) -> schemas.OrgaoResponseDTO:
        nome_normalizado = orgao.nome.strip().lower().capitalize()
        
        # Criar uma execption personalizada se a orgao já existir
        if self.repo.get_orgao_by_name(nome_normalizado):
            raise ValueError(
                f"Orgao with name '{nome_normalizado}' already exists."
            )
        
        orgao_normalizada = schemas.OrgaoRequestDTO(nome=nome_normalizado)
        db_orgao = self.repo.create_orgao(orgao_normalizada)
        
        return schemas.OrgaoResponseDTO.model_validate(db_orgao)

    def get_orgao(self, orgao_id: int) -> schemas.OrgaoResponseDTO:
        db_orgao = self.repo.get_orgao(orgao_id)
        if db_orgao:
            return schemas.OrgaoResponseDTO.model_validate(db_orgao)
        return None

    def get_all_orgaos(self, skip, limit) -> list[schemas.OrgaoResponseDTO]:
        orgaos = self.repo.get_all_orgaos(skip=skip, limit=limit)
        return [schemas.OrgaoResponseDTO.model_validate(d) for d in orgaos]

    def update_orgao(self, orgao_id: int, orgao: schemas.OrgaoRequestDTO) -> schemas.OrgaoResponseDTO:
        nome_normalizado = orgao.nome.strip().lower().capitalize()
        orgao_normalizada = schemas.OrgaoRequestDTO(nome=nome_normalizado)
        
        db_orgao = self.repo.update_orgao(orgao_id, orgao_normalizada)
        if db_orgao:
            return schemas.OrgaoResponseDTO.model_validate(db_orgao)
        return None

    def delete_orgao(self, orgao_id: int) -> bool:
        return self.repo.delete_orgao(orgao_id)