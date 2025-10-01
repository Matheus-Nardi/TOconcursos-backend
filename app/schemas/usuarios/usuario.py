from schemas.cronograma.cronograma import CronogramaResponseDTO
from pydantic import BaseModel
from datetime import datetime

class UsuarioBaseDTO(BaseModel):
    nome: str
    email: str
    cpf: str
    avatar: str | None = None

class UsuarioRequestDTO(UsuarioBaseDTO):
    senha: str

class UsuarioResponseDTO(UsuarioBaseDTO):
    id: int
    data_criacao: datetime
    cronogramas: list[CronogramaResponseDTO] = []

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    