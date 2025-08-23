from pydantic import BaseModel
from datetime import datetime

class ComentarioRequestDTO(BaseModel):
    comentario: str
    data_comentario: datetime
    questao_id: int

class ComentarioResponseDTO(BaseModel):
    id: int
    comentario: str
    data_comentario: datetime
    questao_id: int

    model_config = {
        "from_attributes": True
    }