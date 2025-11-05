from pydantic import BaseModel
from datetime import datetime
from schemas.usuarios.usuario import UsuarioResponseDTO
from schemas.usuarios.estatisticas_usuario import EstatisticasUsuarioDTO
from schemas.usuarios.historico_assinaturas import HistoricoAssinaturasDTO

class ObjetivoResponseDTO(BaseModel):
    id: int
    nome: str
    area: str
    class Config:
        from_attributes = True
    