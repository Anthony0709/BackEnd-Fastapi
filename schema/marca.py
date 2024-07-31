from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MarcaBase(BaseModel):
    descripcion: str
    activo: bool

class MarcaCreate(MarcaBase):
    pass

class Marca(MarcaBase):
    IdMarca: Optional[int] = None
    fechaRegistro: datetime

    class Config:
        from_attributes = True

class MarcaUpdate(BaseModel):
    descripcion: Optional[str] = None
    activo: Optional[bool] = None