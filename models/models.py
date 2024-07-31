<<<<<<< HEAD
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String,func
from sqlalchemy.orm import relationship, configure_mappers

from config.database import Base

class Marca(Base):
    __tablename__ = 'marca'
    IdMarca	= Column(Integer, primary_key=True, index= True)
    descripcion = Column(String(100), nullable=False)
    activo = Column(Boolean, default = 1 )
    fechaRegistro = Column(DateTime, default=func.now(), nullable=False)

    marcas = relationship("Producto", back_populates="marca")

class Categoria(Base):
    __tablename__ = 'categoria'
    IdCategoria	= Column(Integer, primary_key=True, index= True)
    descripcion = Column(String(100), nullable=False)
    activo = Column(Boolean)
    fechaRegistro = Column(DateTime, default=func.now(), nullable=False)

    categorias = relationship("Producto", back_populates="categoria")


class Producto(Base):
    __tablename__ = 'producto'
    idProducto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String, nullable=True)
    idMarca = Column(Integer, ForeignKey('marca.IdMarca'), nullable=False)
    idCategoria = Column(Integer, ForeignKey('categoria.IdCategoria'), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    rutaImagen = Column(String(200), nullable=True)
    nombreImagen = Column(String(100), nullable=True)
    activo = Column(Boolean, nullable=False, default=1)
    fechaRegistro = Column(DateTime, default=func.now(), nullable=False)

    marca = relationship("Marca")
    categoria = relationship("Categoria")

class Usuario(Base):
    __tablename__ = "usuario"
    idUsuario = Column(Integer, primary_key= True, index= True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    correo = Column(String, unique=True, index=True)
    clave = Column(String)
    reestablecer = Column(Boolean, default= False)
    activo	= Column(Boolean, default=1)
    fechaRegistro = Column(DateTime, default=func.now(), nullable=False)
=======
import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String,func
from sqlalchemy.orm import relationship

from config.database import Base

class Marca(Base):
    __tablename__ = 'marca'
    IdMarca	= Column(Integer, primary_key=True, index= True)
    descripcion = Column(String(100), nullable=False)	
    activo = Column(Boolean, default = 1 )
    fechaRegistro = Column(DateTime, default=func.now(), nullable=False)

    marcas = relationship("Producto", back_populates="marca")

class Categoria(Base):
    __tablename__ = 'categoria'
    IdCategoria	= Column(Integer, primary_key=True, index= True)
    descripcion = Column(String(100), nullable=False)	
    activo = Column(Boolean, default = True )
    fechaRegistro = Column(DateTime, default=func.now(), nullable=False)

    categorias = relationship("Producto", back_populates="categoria")


class Producto(Base):
    __tablename__ = 'producto'
    idProducto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String, nullable=True)
    idMarca = Column(Integer, ForeignKey('marca.IdMarca'), nullable=False)
    idCategoria = Column(Integer, ForeignKey('categoria.IdCategoria'), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    rutaImagen = Column(String(200), nullable=True)
    nombreImagen = Column(String(100), nullable=True)
    activo = Column(Boolean, nullable=False, default=1)
    fechaRegistro = Column(DateTime, default=func.now(), nullable=False)

    marca = relationship("Marca")
    categoria = relationship("Categoria")

class Usuario(Base):
    __tablename__ = "usuario" 
    idUsuario = Column(Integer, primary_key= True, index= True)	
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)	
    correo = Column(String, unique=True, index=True)
    clave = Column(String)	
    reestablecer = Column(Boolean, default= False)	
    activo	= Column(Boolean, default=1)
    fechaRegistro = Column(DateTime, default=func.now(), nullable=False)
>>>>>>> aac900737ca7d873e64123d573b37c67115fd7f1
