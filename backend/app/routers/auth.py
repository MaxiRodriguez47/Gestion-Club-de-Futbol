from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user, requiere_admin
from app.schemas.usuario import UsuarioCreate, UsuarioOut, Token
from app.crud import usuario as crud_usuario
from app.auth import crear_access_token

router = APIRouter(prefix="/auth", tags=["Autenticacion"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = crud_usuario.autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contrasena incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = crear_access_token(data={"sub": usuario.username, "rol": usuario.rol.value})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/registrar", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def registrar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    admin_actual=Depends(requiere_admin),
):
    if crud_usuario.get_usuario_por_username(db, usuario.username):
        raise HTTPException(status_code=400, detail="Ese nombre de usuario ya existe")
    return crud_usuario.crear_usuario(db, usuario)

@router.get("/perfil", response_model=UsuarioOut)
def mi_perfil(usuario_actual=Depends(get_current_user)):
    return usuario_actual
