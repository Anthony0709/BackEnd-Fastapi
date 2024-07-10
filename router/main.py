import logging
import os
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from schema import Category
from schema import products
from schema import marca as marke


from config import database
from models import models
from scripts import category
from scripts import marca
from scripts import producto
from router import auth

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.title = 'App_DB_Carrito'
app.version = '1.0.0'

models.Base.metadata.create_all(bind=database.engine)


# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Cambia esto según sea necesario
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",tags=['Mensaje'],dependencies=[Depends(auth.read_usuarios_me)])
async def home():
    return ("Bienvenido APP en ejecucion")

#***************************************************************************

@app.post("/productos/",tags=['Crear'], response_model=products.Producto,dependencies=[Depends(auth.read_usuarios_me)])
async def create_producto(
    nombre: str = Form(...),
    descripcion: str = Form(None),
    idMarca: int = Form(...),
    idCategoria: int = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
    activo: bool = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    print(f"Nombre: {nombre}, Descripción: {descripcion}, ID Marca: {idMarca}, ID Categoría: {idCategoria}, Precio: {precio}, Stock: {stock}, Activo: {activo}")

    try:
        # Crear el directorio si no existe
        os.makedirs("static/images", exist_ok=True)

        # Guardar la imagen
        image_name = image.filename
        image_path = f"static/images/{image_name}"
        print(f"Guardando imagen en: {image_path}")
        with open(image_path, "wb") as image_file:
            image_file.write(await image.read())

        # Crear el objeto ProductoCreate
        producto_data = products.ProductoCreate(
            nombre=nombre,
            descripcion=descripcion,
            idMarca=idMarca,
            idCategoria=idCategoria,
            precio=precio,
            stock=stock,
            activo=activo
        )

        print(f"Datos del producto: {producto_data}")

        # Crear el producto en la base de datos
        db_producto = producto.create_producto(db=db, producto=producto_data, image_path=image_path, image_name=image_name)
        print(f"Producto creado: {db_producto}")
        return db_producto
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/productos/",tags=['Listar'], response_model = List[products.Producto],dependencies=[Depends(auth.read_usuarios_me)])
async def read_productos(skip : int = 0 , limit : int = 10, db : Session = Depends(database.get_db)):
    product = producto.get_productos(db, skip=skip, limit=limit)
    return product

@app.get("/productos/{id}",tags=['Listar por ID'], response_model=products.Producto,dependencies=[Depends(auth.read_usuarios_me)])
async def read_producto(producto_id : int, db : Session = Depends(database.get_db)):
    db_producto = producto.get_producto(db, producto_id = producto_id)
    if db_producto is None:
        raise HTTPException(status_code = 404, detail = "Producto no encontrado")
    return db_producto

@app.put("/productos/{id}",tags=['Actualizar'], response_model=products.ProductoUpdate,dependencies=[Depends(auth.read_usuarios_me)])
async def update_producto(
    producto_id: int,
    nombre: Optional[str] = Form(None),
    descripcion: Optional[str] = Form(None),
    idMarca: Optional[int] = Form(None),
    idCategoria: Optional[int] = Form(None),
    precio: Optional[float] = Form(None),
    stock: Optional[int] = Form(None),
    activo: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(database.get_db)
):
    print(f"Actualizando producto ID: {producto_id}")

    try:
        # Obtener el producto existente de la base de datos
        db_producto = producto.get_producto(db, producto_id)
        if not db_producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        # Actualizar los campos del producto si se proporcionan nuevos valores
        if nombre:
            db_producto.nombre = nombre
        if descripcion:
            db_producto.descripcion = descripcion
        if idMarca:
            db_producto.idMarca = idMarca
        if idCategoria:
            db_producto.idCategoria = idCategoria
        if precio:
            db_producto.precio = precio
        if stock:
            db_producto.stock = stock
        if activo is not None:
            db_producto.activo = activo
        
        # Procesar la nueva imagen si se proporciona
        if image and isinstance(image, UploadFile):
            # Crear el directorio si no existe
            os.makedirs("static/images", exist_ok=True)

            # Guardar la imagen
            image_name = image.filename
            image_path = f"static/images/{image_name}"
            print(f"Guardando nueva imagen en: {image_path}")
            with open(image_path, "wb") as image_file:
                image_file.write(await image.read())
            
            # Actualizar los campos de la imagen en el producto
            db_producto.rutaImagen = image_path
            db_producto.nombreImagen = image_name
        
        
        # Guardar los cambios en la base de datos
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)

        print(f"Producto actualizado: {db_producto}")
        return db_producto

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete('/productos/{id}', tags=['Eliminar'], response_model=dict, status_code=200,dependencies=[Depends(auth.read_usuarios_me)])
def delete_producto(producto_id: int, db: Session = Depends(database.get_db)) -> dict:
    try:
        # Buscar el producto en la base de datos usando el ID proporcionado
        db_producto = producto.get_producto(db, producto_id)
        
        # Si el producto no se encuentra, devolver un mensaje de error con código 404
        if not db_producto:
            return JSONResponse(status_code=404, content={'mensaje': 'Producto no encontrado'})
        
        # Eliminar el producto encontrado
        db.delete(db_producto)
        
        # Confirmar (commitear) la transacción para que los cambios se guarden en la base de datos
        db.commit()
        
        # Devolver una respuesta exitosa indicando que el producto ha sido eliminado
        return JSONResponse(content={'mensaje': 'Producto eliminado'}, status_code=200)
    
    except Exception as e:
        # En caso de que ocurra una excepción, revertir (rollback) los cambios realizados en la base de datos
        db.rollback()
        
        # Registrar el error en los logs para poder investigarlo más tarde
        logger.error(f"Error al eliminar el producto: {e}")
        
        # Lanzar una excepción HTTP 500 indicando un error interno del servidor
        raise HTTPException(status_code=500, detail="Error interno del servidor")

#***************************************************************************

@app.post("/categorias/",tags=['Crear'], response_model=Category.Categoria,dependencies=[Depends(auth.read_usuarios_me)])
async def create_categoria(categoriaSC: Category.CategoriaCreate, db: Session = Depends(database.get_db)):
    db_categoria = category.get_categoria_by_name(db, nombre=categoriaSC.descripcion)
    if db_categoria:
        raise HTTPException(status_code=400, detail="La categoría ya existe")
    return category.create_categoria(db=db, categoria=categoriaSC)

@app.get("/categorias/",tags=['Listar'], response_model= List[Category.Categoria],dependencies=[Depends(auth.read_usuarios_me)])
async def read_categorias(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    categorias = category.get_categorias(db, skip=skip, limit=limit)
    return categorias

@app.get("/categorias/{categoria_id}",tags=['Listar por ID'], response_model=Category.Categoria,dependencies=[Depends(auth.read_usuarios_me)])
async def read_categoria(categoria_id: int, db: Session = Depends(database.get_db)):
    db_categoria = category.get_categoria(db, categoria_id=categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria

@app.delete('/categorias/{id}', tags=['Eliminar'], response_model=dict, status_code=200,dependencies=[Depends(auth.read_usuarios_me)])
def delete_categoria(id: int, db: Session = Depends(database.get_db)) -> dict:
    try:
        # Buscar el categoria en la base de datos usando el ID proporcionado
        db_categoria = category.get_categoria(db, id)
        
        # Si la categoria no se encuentra, devolver un mensaje de error con código 404
        if not db_categoria:
            return JSONResponse(status_code=404, content={'mensaje': 'Categoria no encontrado'})
        
        # Eliminar la categoria encontrado
        db.delete(db_categoria)
        
        # Confirmar (commitear) la transacción para que los cambios se guarden en la base de datos
        db.commit()
        
        # Devolver una respuesta exitosa indicando que la categoria ha sido eliminado
        return JSONResponse(content={'mensaje': 'Categoria eliminada'}, status_code=200)
    
    except Exception as e:
        # En caso de que ocurra una excepción, revertir (rollback) los cambios realizados en la base de datos
        db.rollback()
        
        # Registrar el error en los logs para poder investigarlo más tarde
        logger.error(f"Error al eliminar la categoria: {e}")
        
        # Lanzar una excepción HTTP 500 indicando un error interno del servidor
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.put("/categorias/{categoria_id}",tags=['Actualizar'], response_model=Category.CategoriaUpdate,dependencies=[Depends(auth.read_usuarios_me)])
def actualiza_ventas(id: int, categoria: Category.CategoriaUpdate, db: Session = Depends(database.get_db)) -> dict:
    resultado = db.query(models.Categoria).filter(models.Categoria.IdCategoria == id).first()
    if not resultado:
        return JSONResponse(status_code=404, content={'mensaje': 'No se ha podido actualizar'})
    resultado.descripcion = categoria.descripcion
    resultado.activo = categoria.activo
    db.commit()
    # recorrer los elementos de la lista
    return JSONResponse(content={'mensaje': 'Venta actualizada'}, status_code=201)


"""
def update_categoria(categoria_id: int, categoria: Category.CategoriaUpdate, db: Session = Depends(database.get_db)):
    db_categoria = category.update_categoria(db, categoria_id, categoria)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria
"""




#***************************************************************************

app.include_router(auth.router)

#***************************************************************************

@app.post("/marca/",tags=['Crear'], response_model=marke.Marca,dependencies=[Depends(auth.read_usuarios_me)])
async def create_marca(marcaP: marke.MarcaCreate, db: Session = Depends(database.get_db)):
    db_marca = marca.get_marca_by_name(db, nombre=marcaP.descripcion)
    if db_marca:
        raise HTTPException(status_code=400, detail="La Marca ya existe")
    return marca.create_marca(db=db, marca=marcaP)

@app.get("/marca/",tags=['Listar'], response_model=List[marke.Marca],dependencies=[Depends(auth.read_usuarios_me)])
async def read_marca(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    marcas = marca.get_marcas(db, skip=skip, limit=limit)
    return marcas

@app.get("/marca/{id}",tags=['Listar por ID'], response_model=marke.Marca,dependencies=[Depends(auth.read_usuarios_me)])
async def read_marca(marcas_id: int, db: Session = Depends(database.get_db)):
    db_marca = marca.get_marca(db, marca_id=marcas_id)
    if db_marca is None:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return db_marca

@app.delete("/marca/{id}", tags=['Eliminar'], response_model=dict, status_code=200,dependencies=[Depends(auth.read_usuarios_me)])
def delete_marca(id: int, db: Session = Depends(database.get_db)) -> dict:
    try:
        # Buscar la marca en la base de datos usando el ID proporcionado
        db_marca = marca.get_marca(db, id)
        
        # Si la marca no se encuentra, devolver un mensaje de error con código 404
        if not db_marca:
            return JSONResponse(status_code=404, content={'mensaje': 'Marca no encontrado'})
        
        # Eliminar el usuario encontrado
        db.delete(db_marca)
        
        # Confirmar (commitear) la transacción para que los cambios se guarden en la base de datos
        db.commit()
        
        # Devolver una respuesta exitosa indicando que la marca ha sido eliminado
        return JSONResponse(content={'mensaje': 'Marca eliminado'}, status_code=200)
    
    except Exception as e:
        # En caso de que ocurra una excepción, revertir (rollback) los cambios realizados en la base de datos
        db.rollback()
        
        # Registrar el error en los logs para poder investigarlo más tarde
        logger.error(f"Error al eliminar la marca: {e}")
        
        # Lanzar una excepción HTTP 500 indicando un error interno del servidor
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.put("/marcas/{id}",tags=['Actualizar'], response_model=marke.MarcaUpdate,dependencies=[Depends(auth.read_usuarios_me)])
def update_marca(marca_id: int, marcaS: marke.MarcaUpdate, db: Session = Depends(database.get_db)):
    db_marca = marca.update_marca(db, marca_id, marcaS)
    if not db_marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return db_marca