from sqlalchemy.orm import Session
from models.usuarios.usuario import Usuario
from repository.usuarios.usuario_repository import UsuarioRepository
from schemas.usuarios.usuario import UsuarioRequestDTO, UsuarioResponseDTO, UsuarioUpdateDTO
from utils.security import hash_password, verify_password, create_access_token
from schemas.usuarios import usuario as schemas
from repository.usuarios.objetivo_repository import ObjetivoRepository
from core.exceptions.exception import NotFoundException, UnauthorizedException, ConflictException


class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)
        self.objetivo_repo = ObjetivoRepository(db)

    def create_usuario(self, usuario: UsuarioRequestDTO) -> UsuarioResponseDTO:
        # Verifica se já existe usuário com o mesmo e-mail
        if self.repo.get_usuario_by_email(usuario.email):
            raise ConflictException("E-mail já está em uso")

        # Verifica se já existe usuário com o mesmo CPF (quando informado)
        if usuario.cpf is not None:
            if self.repo.get_usuario_by_cpf(usuario.cpf):
                raise ConflictException("CPF já está em uso")

        db_usuario = Usuario(
            nome=usuario.nome,
            email=usuario.email,
            cpf=usuario.cpf,
            avatar=usuario.avatar,
            senha=hash_password(usuario.senha)
        )
        db_usuario = self.repo.create_usuario(db_usuario)
        return UsuarioResponseDTO.model_validate(db_usuario)

    def get_usuario(self, usuario_id: int) -> schemas.UsuarioResponseDTO:
        db_usuario = self.repo.get_usuario(usuario_id)
        if not db_usuario:
            raise NotFoundException("Usuário não encontrado")
        return schemas.UsuarioResponseDTO.model_validate(db_usuario)

    def get_all_usuarios(self, skip: int, limit: int) -> list[UsuarioResponseDTO]:
        usuarios = self.repo.get_all_usuarios(skip=skip, limit=limit)
        return [UsuarioResponseDTO.model_validate(u) for u in usuarios]

   # No seu UsuarioService
    def update_usuario(self, usuario_id: int, usuario: UsuarioUpdateDTO) -> UsuarioResponseDTO:
        novos_dados = usuario.model_dump(exclude_unset=True)
    
        if 'id_objetivo' in novos_dados and novos_dados['id_objetivo'] is not None:
            db_objetivo = self.objetivo_repo.get_objetivo(novos_dados['id_objetivo'])
            if not db_objetivo:
                raise NotFoundException("Objetivo não encontrado")

        self.repo.update_usuario(usuario_id, novos_dados)
    
        db_usuario_completo = self.repo.get_usuario_com_objetivo(usuario_id)
        if not db_usuario_completo:
            raise NotFoundException("Usuário não encontrado após atualização")
        return UsuarioResponseDTO.model_validate(db_usuario_completo)

    def delete_usuario(self, usuario_id: int) -> bool:
        return self.repo.delete_usuario(usuario_id)
    
    def authenticate_usuario(self, email: str, senha: str) -> str:
        usuarios = self.repo.db.query(Usuario).filter(Usuario.email == email).first()
        if not usuarios or not verify_password(senha, usuarios.senha):
            raise UnauthorizedException("Email ou senha inválidos")
        token_data = {"sub": str(usuarios.id), "email": usuarios.email}
        return create_access_token(token_data)
    
    def create_or_update_google_user(self, google_user_info: dict) -> UsuarioResponseDTO:
        """
        Cria ou atualiza usuário com dados do Google OAuth.
        Se usuário já existe por google_id, atualiza.
        Se usuário já existe por email, vincula google_id.
        Se não existe, cria novo usuário.
        """
        from services.auth_google.auth_google import AuthGoogleService
        
        google_id = google_user_info.get('google_id')
        email = google_user_info.get('email')
        nome = google_user_info.get('nome')
        avatar = google_user_info.get('avatar')
        
        # Verifica se já existe usuário com esse google_id
        usuario_existente = self.repo.get_usuario_by_google_id(google_id)
        
        if usuario_existente:
            # Atualiza dados do usuário existente
            usuario_existente.nome = nome
            if avatar:
                usuario_existente.avatar = avatar
            self.repo.db.commit()
            self.repo.db.refresh(usuario_existente)
            return UsuarioResponseDTO.model_validate(usuario_existente)
        
        # Verifica se já existe usuário com esse email
        usuario_por_email = self.repo.get_usuario_by_email(email)
        
        if usuario_por_email:
            # Vincula google_id à conta existente
            usuario_por_email.id_google = google_id
            usuario_por_email.nome = nome
            if avatar:
                usuario_por_email.avatar = avatar
            self.repo.db.commit()
            self.repo.db.refresh(usuario_por_email)
            return UsuarioResponseDTO.model_validate(usuario_por_email)
        
        # Cria novo usuário
        senha_aleatoria = AuthGoogleService.generate_random_password()
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            cpf=None,  # CPF opcional para usuários OAuth
            avatar=avatar,
            senha=hash_password(senha_aleatoria),
            id_google=google_id
        )
        novo_usuario = self.repo.create_usuario(novo_usuario)
        return UsuarioResponseDTO.model_validate(novo_usuario)
    
    def authenticate_google_user(self, google_user_info: dict) -> str:
        """
        Autentica usuário do Google e retorna JWT token.
        Cria ou atualiza usuário se necessário.
        """
        usuario = self.create_or_update_google_user(google_user_info)
        token_data = {"sub": str(usuario.id), "email": usuario.email}
        return create_access_token(token_data)