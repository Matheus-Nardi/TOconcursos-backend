
import os
import secrets
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()

class AuthGoogleService:
    """Service para autenticação OAuth com Google"""
    
    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        
        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            raise ValueError(
                "Variáveis de ambiente do Google OAuth não configuradas. "
                "Certifique-se de adicionar GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET e "
                "GOOGLE_REDIRECT_URI no arquivo .env"
            )
        
        # Scopes necessários para obter informações do usuário
        self.scopes = [
            'openid',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile'
        ]
    
    def get_authorization_url(self) -> str:
        """
        Gera URL de autorização do Google para redirecionar o usuário.
        
        Returns:
            str: URL de autorização do Google
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.scopes,
            redirect_uri=self.redirect_uri
        )
        
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        return authorization_url
    
    def get_user_info(self, code: str) -> dict:
        """
        Troca o código de autorização por token de acesso e obtém dados do usuário.
        
        Args:
            code: Código de autorização retornado pelo Google após o usuário autorizar
            
        Returns:
            dict: Dicionário com informações do usuário:
                - google_id: ID único do Google
                - email: Email do usuário
                - nome: Nome completo do usuário
                - avatar: URL da foto de perfil (pode ser None)
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.scopes,
            redirect_uri=self.redirect_uri
        )
        
        # Troca o código por token de acesso
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Obter informações do usuário usando a API do Google
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()
        
        return {
            'google_id': user_info.get('id'),
            'email': user_info.get('email'),
            'nome': user_info.get('name'),
            'avatar': user_info.get('picture')
        }
    
    @staticmethod
    def generate_random_password() -> str:
        """
        Gera uma senha aleatória segura para usuários que se autenticam via OAuth.
        
        Returns:
            str: Senha aleatória segura (será hasheada antes de salvar no banco)
        """
        return secrets.token_urlsafe(32)