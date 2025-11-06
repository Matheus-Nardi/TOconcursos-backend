
from schemas.cronograma.cronograma import CronogramaResponseDTO
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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
    objetivo: Optional['ObjetivoResponseDTO'] = None
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UsuarioUpdateDTO(BaseModel):
    nome: Optional[str] = None
    avatar: Optional[str] = None
    id_objetivo: Optional[int] = None

from schemas.usuarios.objetivo import ObjetivoResponseDTO
UsuarioResponseDTO.model_rebuild()