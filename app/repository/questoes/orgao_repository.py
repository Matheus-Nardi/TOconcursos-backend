from sqlalchemy.orm import Session
from models.questoes import orgao as models

class OrgaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, orgao: models.Orgao) -> models.Orgao:
        """
        Salva uma instância de Orgao (cria ou atualiza).
        """
        self.db.add(orgao)
        self.db.commit()
        self.db.refresh(orgao)
        return orgao

    def get_by_id(self, orgao_id: int) -> models.Orgao | None:
        """ Busca um órgão pelo seu ID. """
        return self.db.get(models.Orgao, orgao_id)

    def get_by_name(self, nome: str) -> models.Orgao | None:
        """ Busca um órgão pelo nome. """
        return self.db.query(models.Orgao).filter(models.Orgao.nome == nome).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[models.Orgao]:
        """ 
        Retorna uma lista de órgãos com paginação.
        (Corrigido: unificando os métodos 'get_all_orgaos').
        """
        return self.db.query(models.Orgao).offset(skip).limit(limit).all()

    def delete(self, orgao: models.Orgao) -> None:
        """ Deleta uma instância de Orgao. """
        self.db.delete(orgao)
        self.db.commit()