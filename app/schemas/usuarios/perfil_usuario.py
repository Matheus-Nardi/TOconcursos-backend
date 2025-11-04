from pydantic import BaseModel
from datetime import datetime
from schemas.usuarios.usuario import UsuarioResponseDTO
from schemas.usuarios.estatisticas_usuario import EstatisticasUsuarioDTO
from schemas.usuarios.historico_assinaturas import HistoricoAssinaturasDTO

class PerfilUsuarioCompletoDTO(BaseModel):
    """DTO completo do perfil do usuário contendo informações básicas, 
    estatísticas de uso e histórico de assinaturas."""
    informacoes_basicas: UsuarioResponseDTO
    estatisticas: EstatisticasUsuarioDTO
    assinaturas: HistoricoAssinaturasDTO
    
    class Config:
        from_attributes = True
    