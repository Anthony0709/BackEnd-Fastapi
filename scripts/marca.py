from sqlalchemy.orm import Session
from models import models
from schema import marca

def get_marca_by_name(db: Session, nombre: str):
    return db.query(models.Marca).filter(models.Marca.descripcion == nombre).first()


def create_marca(db: Session, marca: marca.MarcaCreate):
    db_marca = models.Marca(
        descripcion=marca.descripcion,
        activo=marca.activo
    )
    db.add(db_marca)
    db.commit()
    db.refresh(db_marca)
    return db_marca

def get_marcas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Marca).offset(skip).limit(limit).all()

def get_marca(db: Session, marca_id: int):
    return db.query(models.Marca).filter(models.Marca.IdMarca == marca_id).first()

# CRUD para Marca
def update_marca(db: Session, marca_id: int, marca: marca.MarcaUpdate):
    db_marca = db.query(models.Marca).filter(models.Marca.IdMarca == marca_id).first()
    if not db_marca:
        return None
    for key, value in marca.dict(exclude_unset=True).items():
        setattr(db_marca, key, value)
    db.commit()
    db.refresh(db_marca)
    return db_marca