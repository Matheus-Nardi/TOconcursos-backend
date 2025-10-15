from pydantic import BaseModel, Field
from typing import Any, List, Optional

class ErrorDetail(BaseModel):
    """Schema para detalhes de erros de validação."""
    loc: List[str] = Field(..., description="Localização do erro (ex: ['body', 'email'])")
    msg: str = Field(..., description="Mensagem de erro legível.")
    type: str = Field(..., description="Tipo do erro (ex: 'value_error.email').")

class ErrorResponse(BaseModel):
    """Schema padrão para respostas de erro da API."""
    status: str = "error"
    message: str
    path: str
    details: Optional[Any] = None