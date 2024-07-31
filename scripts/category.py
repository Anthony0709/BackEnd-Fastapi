from sqlalchemy.orm import Session
from models import models
from schema import category

def get_categoria_by_name(db: Session, nombre: str):
    return db.query(models.Categoria).filter(models.Categoria.descripcion == nombre).first()


def create_categoria(db: Session, categoria: category.CategoriaCreate):
    db_categoria = models.Categoria(
        descripcion=categoria.descripcion,
        activo=categoria.activo
    )
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def get_categorias(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Categoria).offset(skip).limit(limit).all()

def get_categoria(db: Session, categoria_id: int):
    return db.query(models.Categoria).filter(models.Categoria.IdCategoria == categoria_id).first()

def update_categoria(db: Session, categoria_id: int, categoria: category.CategoriaUpdate):
    db_categoria = db.query(models.Categoria).filter(models.Categoria.IdCategoria == categoria_id).first()
    if not db_categoria:
        return None
    for key, value in categoria.dict(exclude_unset=True).items():
        setattr(db_categoria, key, value)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria