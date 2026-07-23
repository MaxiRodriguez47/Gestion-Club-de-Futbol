from pydantic import BaseModel, Field
from typing import Optional
from app.models.usuario import RolEnum

class UsuarioCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    rol: RolEnum = RolEnum.SOCIO
    socio_id: Optional[int] = None

class UsuarioOut(BaseModel):
    id: int
    username: str
    rol: RolEnum
    activo: bool
    socio_id: Optional[int] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    rol: Optional[str] = None
