from sqlalchemy.orm import Session
from sqlalchemy import func
from models.usuarios.usuario import Usuario
from repository.usuarios.usuario_repository import UsuarioRepository
from schemas.usuarios.usuario import UsuarioRequestDTO, UsuarioResponseDTO
from utils.security import hash_password, verify_password, create_access_token
from schemas.usuarios import usuario as schemas
from core.exceptions.exception import NotFoundException
from repository.pagamento.pagamento_repository import PagamentoRepository
from schemas.usuarios.perfil_usuario import PerfilUsuarioCompletoDTO
from schemas.usuarios.estatisticas_usuario import EstatisticasUsuarioDTO
from schemas.usuarios.historico_assinaturas import HistoricoAssinaturasDTO
from schemas.planos.plano import PlanoResponseDTO, PlanoSimplificadoDTO
from services.upload.upload_service import UploadService
from datetime import datetime
import uuid
from mimetypes import guess_extension

class PerfilUsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)
        self.upload_service = UploadService()
        self.pagamentos_repo = PagamentoRepository(db)
        self.db = db

    def get_perfil_usuario(self, usuario_id: int) -> PerfilUsuarioCompletoDTO:
        """
        Retorna o perfil completo do usuário com informações básicas,
        estatísticas de uso e histórico de assinaturas.
        """
        # 1. Buscar o usuário
        db_usuario = self.repo.get_usuario(usuario_id)
        if not db_usuario:
            raise NotFoundException("Usuário não encontrado")
        
        # 2. Montar informações básicas
        informacoes_basicas = UsuarioResponseDTO.model_validate(db_usuario)
        
        # 3. Calcular estatísticas
        estatisticas = self._calcular_estatisticas(db_usuario)
        
        # 4. Buscar histórico de assinaturas
        assinaturas = self._obter_historico_assinaturas(usuario_id)
        
        # 5. Montar e retornar o DTO completo
        return PerfilUsuarioCompletoDTO(
            informacoes_basicas=informacoes_basicas,
            estatisticas=estatisticas,
            assinaturas=assinaturas
        )
    
    def _calcular_estatisticas(self, usuario: Usuario) -> EstatisticasUsuarioDTO:
        """
        Calcula as estatísticas de uso do usuário baseado em suas resoluções de questões.
        """
        # Obter todas as resoluções de questões do usuário
        resolucoes = usuario.resolucoes_questoes
        
        total_questoes = len(resolucoes)
        total_acertos = sum(1 for r in resolucoes if r.is_certa)
        total_erros = total_questoes - total_acertos
        
        # Calcular percentual de acerto
        percentual_acerto = (total_acertos / total_questoes * 100) if total_questoes > 0 else 0.0
        
        # Total de cronogramas
        total_cronogramas = len(usuario.cronogramas)
        
        # Última atividade (última resolução de questão)
        ultima_atividade = None
        if resolucoes:
            ultima_atividade = max(r.data_resolucao for r in resolucoes)
        
        # Calcular dias consecutivos (streak)
        dias_consecutivos = self._calcular_dias_consecutivos(resolucoes)
        
        return EstatisticasUsuarioDTO(
            total_questoes_resolvidas=total_questoes,
            total_acertos=total_acertos,
            total_erros=total_erros,
            percentual_acerto=round(percentual_acerto, 2),
            total_cronogramas=total_cronogramas,
            dias_consecutivos_estudo=dias_consecutivos,
            ultima_atividade=ultima_atividade
        )
    
    def _calcular_dias_consecutivos(self, resolucoes: list) -> int:
        """
        Calcula quantos dias consecutivos o usuário estudou (resolveu questões).
        """
        if not resolucoes:
            return 0
        
        # Ordenar resoluções por data (mais recente primeiro)
        datas_unicas = sorted(
            set(r.data_resolucao.date() for r in resolucoes),
            reverse=True
        )
        
        if not datas_unicas:
            return 0
        
        # Verificar se estudou hoje ou ontem
        hoje = datetime.now().date()
        data_mais_recente = datas_unicas[0]
        
        dias_diferenca = (hoje - data_mais_recente).days
        
        # Se não estudou hoje nem ontem, streak quebrado
        if dias_diferenca > 1:
            return 0
        
        # Contar dias consecutivos
        streak = 1
        for i in range(1, len(datas_unicas)):
            diferenca = (datas_unicas[i-1] - datas_unicas[i]).days
            if diferenca == 1:
                streak += 1
            else:
                break
        
        return streak
    
    def _obter_historico_assinaturas(self, usuario_id: int) -> HistoricoAssinaturasDTO:
        """
        Obtém o plano atual e o histórico de todos os planos/assinaturas do usuário.
        """
        # Buscar todos os pagamentos do usuário ordenados por data (mais recente primeiro)
        pagamentos = self.pagamentos_repo.get_pagamentos_by_usuario(usuario_id)
        
        if not pagamentos:
            return HistoricoAssinaturasDTO(
                plano_atual=None,
                historico_assinaturas=[]
            )
        
        # Converter pagamentos em planos
        planos = []
        for pagamento in pagamentos:
            if pagamento.plano:
                planos.append(PlanoSimplificadoDTO.model_validate(pagamento.plano))

        # O plano atual é o mais recente
        plano_atual = planos[0] if planos else None
        
        return HistoricoAssinaturasDTO(
            plano_atual=plano_atual,
            historico_assinaturas=planos
        )
    
    def upload_avatar(self, usuario_id: int, file) -> str:
        db_usuario = self.repo.get_usuario(usuario_id)
        if not db_usuario:
            raise NotFoundException("Usuário não encontrado")

        if db_usuario.avatar:
           self.remover_avatar(usuario_id)
           
        arquivo_uuid = str(uuid.uuid4())

   
        extensao = guess_extension(file.content_type) or '.png'

        extensao = extensao.lstrip('.')

        file_bytes = file.file.read()
        file_url = self.upload_service.upload_file(
            file_path=f"avatars/{arquivo_uuid}.{extensao}",
            file_data=file_bytes,
            content_type=file.content_type
    )

        updated_user = self.repo.update_avatar(usuario_id, file_url)
        return updated_user.avatar
    
    def remover_avatar(self, usuario_id: int) -> None:
        db_usuario = self.repo.get_usuario(usuario_id)
        if not db_usuario:
            raise NotFoundException("Usuário não encontrado")

        if not db_usuario.avatar:
            raise ValueError("Usuário não possui avatar para remover")

        file_path = self.upload_service.get_file_path_from_url(db_usuario.avatar)
        self.upload_service.delete_file(file_path)
        self.repo.update_avatar(usuario_id, None)

