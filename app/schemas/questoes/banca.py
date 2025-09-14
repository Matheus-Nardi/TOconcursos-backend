from pydantic import BaseModel

class BancaRequestDTO(BaseModel):
    label: str
    
class BancaResponseDTO(BaseModel):
    id: int
    label: str

    model_config = {
        "from_attributes": True
    }
        
        
        