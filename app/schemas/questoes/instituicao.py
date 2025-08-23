from pydantic import BaseModel

class InstituicaoRequestDTO(BaseModel):
    nome: str
    
class InstituicaoResponseDTO(BaseModel):
    id: int
    nome: str

    model_config = {
        "from_attributes": True
    }
        
        
        