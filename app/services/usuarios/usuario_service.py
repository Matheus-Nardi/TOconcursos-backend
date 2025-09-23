import secrets
from datetime import datetime, timedelta, timezone
from utils.email_sender import send_reset_email
from sqlalchemy.orm import Session
from models.usuarios.usuario import Usuario
from repository.usuarios.usuario_repository import UsuarioRepository
from schemas.usuarios.usuario import UsuarioRequestDTO, UsuarioResponseDTO
from utils.security import hash_password, verify_password, create_access_token

class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def create_usuario(self, usuario: UsuarioRequestDTO) -> dict:
        db_usuario = Usuario(
            nome=usuario.nome,
            email=usuario.email,
            cpf=usuario.cpf,
            avatar=usuario.avatar,
            senha=hash_password(usuario.senha)
        )
        db_usuario = self.repo.create_usuario(db_usuario)
        return UsuarioResponseDTO.model_validate(db_usuario).model_dump(mode="json")

    def get_usuario(self, usuario_id: int) -> dict | None:
        db_usuario = self.repo.get_usuario(usuario_id)
        if db_usuario:
            return UsuarioResponseDTO.model_validate(db_usuario).model_dump(mode="json")
        return None

    def get_all_usuarios(self, skip: int, limit: int) -> list[dict]:
        usuarios = self.repo.get_all_usuarios(skip=skip, limit=limit)
        return [UsuarioResponseDTO.model_validate(u).model_dump(mode="json") for u in usuarios]

    def update_usuario(self, usuario_id: int, usuario: UsuarioRequestDTO) -> dict | None:
        novos_dados = usuario.model_dump(mode="json")
        db_usuario = self.repo.update_usuario(usuario_id, novos_dados)
        if db_usuario:
            return UsuarioResponseDTO.model_validate(db_usuario).model_dump(mode="json")
        return None

    def delete_usuario(self, usuario_id: int) -> bool:
        return self.repo.delete_usuario(usuario_id)
    
    def authenticate_usuario(self, email: str, senha: str) -> str | None:
        usuarios = self.repo.db.query(Usuario).filter(Usuario.email == email).first()
        if usuarios and verify_password(senha, usuarios.senha):
            token_data = {"sub": str(usuarios.id), "email": usuarios.email}
            return create_access_token(token_data)
        return None
    
    # NOVO MÉTODO 👇
    async def request_password_reset(self, email: str):
        """Gera um token de reset e o envia por e-mail."""
        usuario = self.repo.get_usuario_by_email(email)
        if not usuario:
            # Para evitar que um atacante descubra e-mails válidos,
            # não retornamos um erro. A operação simplesmente termina.
            return

        # Gera um código seguro e aleatório
        reset_token = secrets.token_urlsafe(32)
        
        # Define o tempo de expiração (e.g., 15 minutos)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)

        usuario.reset_token = reset_token
        usuario.reset_token_expires = expires_at
        
        self.repo.db.commit()

        await send_reset_email(recipient_email=usuario.email, reset_code=reset_token)

    # NOVO MÉTODO 👇
    def reset_password(self, token: str, new_password: str) -> bool:
        """Valida o token e redefine a senha do usuário."""
        usuario = self.repo.get_usuario_by_reset_token(token)

        # Verifica se o token existe e se não expirou
        if not usuario or usuario.reset_token_expires is None or usuario.reset_token_expires < datetime.utcnow():
            return False

        # Atualiza a senha e invalida o token
        usuario.senha = hash_password(new_password)
        usuario.reset_token = None
        usuario.reset_token_expires = None
        
        self.repo.db.commit()
        return True
