from pydantic import BaseModel
from typing import Optional, Literal

class CartaoRequestDTO(BaseModel):
   
    numero: str
    validade: str  # MM/AA
    nome_titular: str
    codigo_seguranca: str
    
    model_config = {
        "from_attributes": True
    }

class CartaoResponseDTO(BaseModel):
    numero: str
    validade: str  # MM/AA
    nome_titular: str

    model_config = {
        "from_attributes": True,
        "exclude_none": True
    }
