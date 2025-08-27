from pydantic import BaseModel

class InstituicaoRequestDTO(BaseModel):
    label: str
    
class InstituicaoResponseDTO(BaseModel):
    id: int
    label: str

    model_config = {
        "from_attributes": True
    }
        
        
        