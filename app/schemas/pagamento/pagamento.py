from pydantic import BaseModel
from typing import Optional, Literal
from schemas.pagamento.cartao import CartaoRequestDTO, CartaoResponseDTO
from datetime import datetime

class PagamentoRequestDTO(BaseModel):
    id_plano: int
    tipo: Literal["pix", "boleto", "cartao"]  
    valor: float
    chave_pix: Optional[str] = None
    codigo_barras: Optional[str] = None
    cartao: Optional[CartaoRequestDTO] = None
    
    model_config = {
        "from_attributes": True
    }

class PagamentoResponseDTO(BaseModel):
    id: int
    id_plano: int
    tipo: Literal["pix", "boleto", "cartao"]  
    valor: float
    data_pagamento: datetime
    chave_pix: Optional[str] = None
    codigo_barras: Optional[str] = None
    cartao: Optional[CartaoResponseDTO] = None

    
    model_config = {
        "from_attributes": True
    }