from pydantic import BaseModel
from typing import Optional, Literal

class PagamentoRequestDTO(BaseModel):
    id_plano: int
    tipo: Literal["pix", "boleto"]  

    chave_pix: Optional[str] = None
    codigo_barras: Optional[str] = None

    
    model_config = {
        "from_attributes": True
    }

class PagamentoResponseDTO(BaseModel):
    id: int
    id_plano: int
    tipo: Literal["pix", "boleto"]  

    chave_pix: Optional[str] = None
    codigo_barras: Optional[str] = None

    
    model_config = {
        "from_attributes": True
    }