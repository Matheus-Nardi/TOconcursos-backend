from sqlalchemy.orm import Session
from models.usuarios.usuario import Usuario
from repository.usuarios.usuario_repository import UsuarioRepository
from schemas.usuarios.usuario import UsuarioRequestDTO, UsuarioResponseDTO

class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def create_usuario(self, usuario: UsuarioRequestDTO) -> dict:
        db_usuario = Usuario(
            nome=usuario.nome,
            email=usuario.email,
            cpf=usuario.cpf,
            avatar=usuario.avatar,
            senha=usuario.senha
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
