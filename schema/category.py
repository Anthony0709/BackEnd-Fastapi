from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoriaBase(BaseModel):
    descripcion: str
    activo: bool

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    IdCategoria: Optional[int] = None
    fechaRegistro: datetime

    class Config:
        from_attributes = True

class CategoriaUpdate(BaseModel):
    descripcion: Optional[str] = None
    activo: Optional[bool] = None