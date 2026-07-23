from pydantic import BaseModel, Field
from typing import Optional
from app.models.jugador import PosicionEnum, CategoriaEnum

class JugadorBase(BaseModel):
    nombre_completo: str = Field(..., min_length=3, max_length=100)
    posicion: PosicionEnum
    numero_camiseta: int = Field(..., ge=1, le=99)
    categoria: CategoriaEnum
    fecha_nacimiento: Optional[str] = None

class JugadorCreate(JugadorBase):
    pass

class JugadorUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    posicion: Optional[PosicionEnum] = None
    numero_camiseta: Optional[int] = Field(None, ge=1, le=99)
    categoria: Optional[CategoriaEnum] = None
    fecha_nacimiento: Optional[str] = None
    activo: Optional[bool] = None

class JugadorOut(JugadorBase):
    id: int
    activo: bool

    class Config:
        from_attributes = True  # antes: orm_mode = True (Pydantic v1)