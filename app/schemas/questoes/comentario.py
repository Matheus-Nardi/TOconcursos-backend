from pydantic import BaseModel
from datetime import datetime
from schemas.usuarios.usuario import UsuarioResponseDTO

class ComentarioRequestDTO(BaseModel):
    comentario: str
    data_comentario: datetime
    id_questao: int

class ComentarioResponseDTO(BaseModel):
    id: int
    comentario: str
    data_comentario: datetime
    id_questao: int
    usuario:UsuarioResponseDTO

    model_config = {
        "from_attributes": True
    }