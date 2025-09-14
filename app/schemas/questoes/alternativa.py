from pydantic import BaseModel

class AlternativaRequestDTO(BaseModel):
    descricao: str
    is_correta: bool

class AlternativaResponseDTO(BaseModel):
    id: int
    descricao: str
    is_correta: bool
    
    model_config = {
        "from_attributes": True
    }