from datetime import timedelta, datetime as dt
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from jose import JWTError, jwt
from config import database
from schema import usuario as schemas
from scripts import usuario as usuarioScript

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 12

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return usuarioScript.pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return usuarioScript.pwd_context.hash(password)


def authenticate_usuario(db: Session, correo: str, clave: str):
    usuario = usuarioScript.get_usuario_by_correo(db, correo)
    if not usuario or not usuarioScript.pwd_context.verify(clave, usuario.clave):
        return False
    return usuario


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = dt.utcnow() + expires_delta
    else:
        expire = dt.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get("/usuarios/me", tags=['Usuario'], response_model=schemas.Usuario)
async def read_usuarios_me(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pueden validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    usuario = usuarioScript.get_usuario_by_correo(db, correo=correo)
    if usuario is None:
        raise credentials_exception
    return usuario


@router.post("/usuarios/", tags=['Usuario'], response_model=schemas.Usuario, dependencies=[Depends(read_usuarios_me)])
async def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    db_usuario = usuarioScript.get_usuario_by_correo(db, correo=usuario.correo)
    if db_usuario:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    return usuarioScript.create_usuario(db=db, usuario=usuario)


@router.post("/token", tags=['Usuario'], response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(database.get_db)):
    print(
        f"Received login request with username: {form_data.username}, password: {form_data.password}")  # Print the username and password
    usuario = authenticate_usuario(db, form_data.username, form_data.password)

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.correo}
        # , expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/usuarios/{usuario_id}", tags=['Usuario'], response_model=schemas.Usuario,
         dependencies=[Depends(read_usuarios_me)])
async def read_usuario(usuario_id: int, db: Session = Depends(database.get_db)):
    db_user = usuarioScript.get_usuario_by_ID(db, usuario_id=usuario_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrada")
    return db_user


@router.get("/usuarios/", tags=['Usuario'], response_model=List[schemas.Usuario],
            dependencies=[Depends(read_usuarios_me)])
async def read_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    usuario = usuarioScript.get_usuarios(db, skip=skip, limit=limit)
    return usuario


@router.delete('/usuarios/{id}', tags=['Usuario'], response_model=dict, status_code=200,
               dependencies=[Depends(read_usuarios_me)])
def delete_usuario(id: int, db: Session = Depends(database.get_db)) -> dict:
    try:
        # Buscar el usuario en la base de datos usando el ID proporcionado
        db_usuario = usuarioScript.get_usuario_by_ID(db, id)

        # Si el usuario no se encuentra, devolver un mensaje de error con código 404
        if not db_usuario:
            return JSONResponse(status_code=404, content={'mensaje': 'Usuario no encontrado'})

        # Eliminar el usuario encontrado
        db.delete(db_usuario)

        # Confirmar (commitear) la transacción para que los cambios se guarden en la base de datos
        db.commit()

        # Devolver una respuesta exitosa indicando que la usuario ha sido eliminado
        return JSONResponse(content={'mensaje': 'usuario eliminada'}, status_code=200)

    except Exception as e:
        # En caso de que ocurra una excepción, revertir (rollback) los cambios realizados en la base de datos
        db.rollback()

        # Registrar el error en los logs para poder investigarlo más tarde
        logger.error(f"Error al eliminar la categoria: {e}")

        # Lanzar una excepción HTTP 500 indicando un error interno del servidor
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/usuarios/{user_id}", tags=['Usuario'], response_model=schemas.UsuarioUpdate,
            dependencies=[Depends(read_usuarios_me)])
def update_usuario(user_id: int, user: schemas.UsuarioUpdate, db: Session = Depends(database.get_db)):
    db_usuario = usuarioScript.update_usuario(db, user_id, user)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrada")
    return db_usuario

