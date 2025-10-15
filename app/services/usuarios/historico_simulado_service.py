from sqlalchemy.orm import Session
from models.usuarios.historico_simulado import HistoricoSimulado
from repository.usuarios.historico_simulado_repository import HistoricoSimuladoRepository
from schemas.usuarios.historico_simulado import HistoricoSimuladoRequestDTO, HistoricoSimuladoResponseDTO
from datetime import datetime
from core.exceptions.exception import NotFoundException

class HistoricoSimuladoService:
    def __init__(self, db: Session):
        self.repo = HistoricoSimuladoRepository(db)

    def create_historico(self, historico: HistoricoSimuladoRequestDTO) -> dict:
        db_historico = HistoricoSimulado(
            usuario_id=historico.usuario_id,
            data_resolucao=historico.data_resolucao or datetime.utcnow()
        )
        db_historico = self.repo.create_historico(db_historico)
        return HistoricoSimuladoResponseDTO.model_validate(db_historico).model_dump(mode="json")

    def get_historico(self, historico_id: int) -> dict:
        db_historico = self.repo.get_historico(historico_id)
        if not db_historico:
            raise NotFoundException("Histórico de simulado não encontrado")
        return HistoricoSimuladoResponseDTO.model_validate(db_historico).model_dump(mode="json")

    def get_all_historicos(self, skip: int, limit: int) -> list[dict]:
        historicos = self.repo.get_all_historicos(skip=skip, limit=limit)
        return [HistoricoSimuladoResponseDTO.model_validate(h).model_dump(mode="json") for h in historicos]

    def update_historico(self, historico_id: int, historico: HistoricoSimuladoRequestDTO) -> dict:
        novos_dados = historico.model_dump(mode="json")
        db_historico = self.repo.update_historico(historico_id, novos_dados)
        if not db_historico:
            raise NotFoundException("Histórico de simulado não encontrado")
        return HistoricoSimuladoResponseDTO.model_validate(db_historico).model_dump(mode="json")

    def delete_historico(self, historico_id: int) -> bool:
        return self.repo.delete_historico(historico_id)
