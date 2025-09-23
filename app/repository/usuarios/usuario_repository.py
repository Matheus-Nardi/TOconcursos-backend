from sqlalchemy.orm import Session
from models.usuarios.usuario import Usuario

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_usuario(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def get_usuario(self, usuario_id: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    def get_all_usuarios(self, skip: int = 0, limit: int = 10) -> list[Usuario]:
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def update_usuario(self, usuario_id: str, novos_dados: dict) -> Usuario | None:
        usuario = self.get_usuario(usuario_id)
        if not usuario:
            return None
        for campo, valor in novos_dados.items():
            setattr(usuario, campo, valor)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete_usuario(self, usuario_id: str) -> bool:
        usuario = self.get_usuario(usuario_id)
        if not usuario:
            return False
        self.db.delete(usuario)
        self.db.commit()
        return True
    
    def get_usuario_by_email(self, email: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def get_usuario_by_reset_token(self, token: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.reset_token == token).first()
