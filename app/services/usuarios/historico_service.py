from sqlalchemy.orm import Session
from models.usuarios.historico import Historico
from repository.usuarios.historico_repository import HistoricoRepository
from schemas.usuarios.historico import HistoricoRequestDTO, HistoricoResponseDTO

class HistoricoService:
    def __init__(self, db: Session):
        self.repo = HistoricoRepository(db)

    def create_historico(self, historico: HistoricoRequestDTO) -> HistoricoResponseDTO:
        db_historico = Historico(
            dias_sequencia=historico.dias_sequencia,
            usuario_id=historico.usuario_id
        )
        db_historico = self.repo.create_historico(db_historico)
        return HistoricoResponseDTO.model_validate(db_historico)

    def get_historico(self, historico_id: int) -> HistoricoResponseDTO | None:
        db_historico = self.repo.get_historico(historico_id)
        if db_historico:
            return HistoricoResponseDTO.model_validate(db_historico)
        return None

    def get_all_historicos(self, skip: int, limit: int) -> list[HistoricoResponseDTO]:
        historicos = self.repo.get_all_historicos(skip=skip, limit=limit)
        return [HistoricoResponseDTO.model_validate(h) for h in historicos]

    def update_historico(self, historico_id: int, historico: HistoricoRequestDTO) -> HistoricoResponseDTO | None:
        novos_dados = historico.model_dump()
        db_historico = self.repo.update_historico(historico_id, novos_dados)
        if db_historico:
            return HistoricoResponseDTO.model_validate(db_historico)
        return None

    def delete_historico(self, historico_id: int) -> bool:
        return self.repo.delete_historico(historico_id)
