from pydantic import BaseModel

class OrgaoRequestDTO(BaseModel):
    nome: str
    
class OrgaoResponseDTO(BaseModel):
    id: int
    nome: str

    model_config = {
        "from_attributes": True
    }
        
        
        