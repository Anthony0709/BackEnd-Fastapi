from sqlalchemy.orm import Session
from models import models
from schema import usuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_usuario_by_correo(db: Session, correo: str):
    return db.query(models.Usuario).filter(models.Usuario.correo == correo).first()

def get_usuario_by_ID(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.idUsuario == usuario_id).first()

def create_usuario(db: Session, usuario: usuario.UsuarioCreate):
    hashed_clave = pwd_context.hash(usuario.clave)
    db_usuario = models.Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        correo=usuario.correo,
        clave=hashed_clave,
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


# CRUD para usuario
def update_usuario(db: Session, user_id: int, user: usuario.UsuarioUpdate):
    db_user = db.query(models.Usuario).filter(models.Usuario.idUsuario == user_id).first()
    if not db_user:
        return None
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user