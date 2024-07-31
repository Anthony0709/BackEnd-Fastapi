from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    idMarca: int
    idCategoria: int
    precio: float
    stock: int
    activo: bool


class ProductoCreate(ProductoBase):
    pass


class Producto(ProductoBase):
    idProducto: Optional[int] = None
    rutaImagen: Optional[str] = None
    nombreImagen: Optional[str] = None
    fechaRegistro: datetime  # O datetime si es aplicable

    class Config:
        from_attributes = True


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    idMarca: Optional[int] = None
    idCategoria: Optional[int] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    activo: Optional[bool] = None
    rutaImagen: Optional[str] = None
    nombreImagen: Optional[str] = None