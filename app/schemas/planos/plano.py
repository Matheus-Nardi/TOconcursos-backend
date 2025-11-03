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