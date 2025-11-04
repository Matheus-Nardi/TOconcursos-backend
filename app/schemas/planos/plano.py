from pydantic import BaseModel
from typing import List

class PlanoResponseDTO(BaseModel):
    id: int
    nome: str
    descricao: str
    valor: float
    beneficios: List[str]   
    
    model_config = {
        "from_attributes": True
    }

class PlanoSimplificadoDTO(BaseModel):
    id: int
    nome: str
    valor: float

    model_config = {
        "from_attributes": True
    }