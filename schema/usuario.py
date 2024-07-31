<<<<<<< HEAD
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre : str
    apellido : str
    correo : EmailStr

class UsuarioCreate(UsuarioBase):
    clave : str

class Usuario(UsuarioBase):
    idUsuario : Optional[int] = None
    reestablecer : bool
    activo : bool
    fechaRegistro : datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UsuarioUpdate(BaseModel):
    nombre : Optional[str] = None
    apellido : Optional[str] = None
    correo : Optional[EmailStr] = None
    clave : Optional[str] = None
    reestablecer : Optional[bool] = None
=======
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre : str
    apellido : str 
    correo : EmailStr

class UsuarioCreate(UsuarioBase):
    clave : str

class Usuario(UsuarioBase):
    idUsuario : Optional[int] = None
    reestablecer : bool
    activo : bool
    fechaRegistro : datetime

    class Config: 
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UsuarioUpdate(BaseModel):
    nombre : Optional[str] = None
    apellido : Optional[str] = None
    correo : Optional[EmailStr] = None
    clave : Optional[str] = None
    reestablecer : Optional[bool] = None
>>>>>>> aac900737ca7d873e64123d573b37c67115fd7f1
    activo : Optional[bool] = None