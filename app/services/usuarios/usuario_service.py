from sqlalchemy.orm import Session
from models.usuarios.usuario import Usuario
from repository.usuarios.usuario_repository import UsuarioRepository
from schemas.usuarios.usuario import UsuarioRequestDTO, UsuarioResponseDTO
from utils.security import hash_password, verify_password, create_access_token
from schemas.usuarios import usuario as schemas
from core.exceptions.exception import NotFoundException, UnauthorizedException
class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def create_usuario(self, usuario: UsuarioRequestDTO) -> UsuarioResponseDTO:
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

    def update_usuario(self, usuario_id: int, usuario: UsuarioRequestDTO) -> UsuarioResponseDTO:
        novos_dados = usuario.model_dump()
        db_usuario = self.repo.update_usuario(usuario_id, novos_dados)
        if not db_usuario:
            raise NotFoundException("Usuário não encontrado")
        return UsuarioResponseDTO.model_validate(db_usuario)

    def delete_usuario(self, usuario_id: int) -> bool:
        return self.repo.delete_usuario(usuario_id)
    
    def authenticate_usuario(self, email: str, senha: str) -> str:
        usuarios = self.repo.db.query(Usuario).filter(Usuario.email == email).first()
        if not usuarios or not verify_password(senha, usuarios.senha):
            raise UnauthorizedException("Email ou senha inválidos")
        token_data = {"sub": str(usuarios.id), "email": usuarios.email}
        return create_access_token(token_data)
