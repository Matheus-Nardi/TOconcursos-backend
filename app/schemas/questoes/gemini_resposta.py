from pydantic import BaseModel

class GeminiRespostaResponseDTO(BaseModel):
    """Schema para resposta gerada pelo Gemini"""
    resposta: str
    questao_id: int

