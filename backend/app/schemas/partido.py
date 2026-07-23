from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.partido import CondicionEnum

class PartidoBase(BaseModel):
    rival: str = Field(..., min_length=2, max_length=100)
    fecha: datetime
    condicion: CondicionEnum
    torneo: Optional[str] = None

class PartidoCreate(PartidoBase):
    pass

class PartidoUpdate(BaseModel):
    rival: Optional[str] = None
    fecha: Optional[datetime] = None
    condicion: Optional[CondicionEnum] = None
    torneo: Optional[str] = None

class RegistrarResultado(BaseModel):
    goles_favor: int = Field(..., ge=0)
    goles_contra: int = Field(..., ge=0)

class PartidoOut(PartidoBase):
    id: int
    goles_favor: Optional[int] = None
    goles_contra: Optional[int] = None
    jugado: bool

    class Config:
        from_attributes = True