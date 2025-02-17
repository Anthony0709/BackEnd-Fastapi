from typing import Optional
from sqlalchemy.orm import Session

from models import models
from schema import products

def create_producto(db: Session, producto: products.ProductoCreate, image_path: str, image_name: str):
    db_producto = models.Producto(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        idMarca=producto.idMarca,
        idCategoria=producto.idCategoria,
        precio=producto.precio,
        stock=producto.stock,
        rutaImagen=image_path,
        nombreImagen=image_name,
        activo=producto.activo,
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto
    #return {"mensaje": "registrado"}

def get_productos(db : Session, skip : int, limit : int = 10 ):
    return db.query(models.Producto).offset(skip).limit(limit).all()

def get_producto(db : Session, producto_id : int ):
    return db.query(models.Producto).filter(models.Producto.idProducto == producto_id).first()


def update_producto(db: Session, producto_id: int, producto: products.ProductoUpdate, image_path: Optional[str] = None, image_name: Optional[str] = None):
    db_producto = db.query(models.Producto).filter(models.Producto.idProducto == producto_id).first()
    if db_producto is None:
        return None
    for key, value in producto.dict(exclude_unset=True).items():
        setattr(db_producto, key, value)
    if image_path:
        db_producto.rutaImagen = image_path
    if image_name:
        db_producto.nombreImagen = image_name
    db.commit()
    db.refresh(db_producto)
    return db_producto