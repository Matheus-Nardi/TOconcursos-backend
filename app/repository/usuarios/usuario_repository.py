from sqlalchemy.orm import Session
from models.usuarios.usuario import Usuario
from sqlalchemy.orm import joinedload
class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_usuario(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def get_usuario(self, usuario_id: int) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    

    def get_all_usuarios(self, skip: int = 0, limit: int = 10) -> list[Usuario]:
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def update_usuario(self, usuario_id: int, novos_dados: dict) -> Usuario | None:
        usuario = self.get_usuario(usuario_id)
        if not usuario:
            return None
        for campo, valor in novos_dados.items():
            setattr(usuario, campo, valor)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete_usuario(self, usuario_id: int) -> bool:
        usuario = self.get_usuario(usuario_id)
        if not usuario:
            return False
        self.db.delete(usuario)
        self.db.commit()
        return True
    
    def get_usuario_com_objetivo(self, usuario_id: int) -> Usuario | None:
        return (
            self.db.query(Usuario)
            .options(joinedload(Usuario.objetivo))
            .filter(Usuario.id == usuario_id)
            .first()
        )
