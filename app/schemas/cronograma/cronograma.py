from pydantic import BaseModel
from datetime import datetime
from models.cronograma.dia_da_semana import DiaDaSemanaEnum
from schemas.cronograma.estudo_diario import EstudoDiarioRequestDTO, EstudoDiarioResponseDTO

class CronogramaRequestDTO(BaseModel):
    nome: str
    descricao: str
    estudos_diarios: list[EstudoDiarioRequestDTO]

class CronogramaResponseDTO(BaseModel):
    id: int
    nome: str
    descricao: str
    data_criacao: datetime
    estudos_diarios: list[EstudoDiarioResponseDTO]

    model_config = {
        "from_attributes": True
    }