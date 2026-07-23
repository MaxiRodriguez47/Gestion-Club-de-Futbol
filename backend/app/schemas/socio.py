from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date

class SocioBase(BaseModel):
    nombre_completo: str = Field(..., min_length=3, max_length=100)
    dni: str = Field(..., min_length=6, max_length=20)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    categoria_socio: str = "General"
    monto_cuota: float = Field(0.0, ge=0)

class SocioCreate(SocioBase):
    fecha_ingreso: date

class SocioUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    categoria_socio: Optional[str] = None
    monto_cuota: Optional[float] = Field(None, ge=0)
    activo: Optional[bool] = None

class RegistrarPago(BaseModel):
    fecha_pago: date = Field(default_factory=date.today)

class SocioOut(SocioBase):
    id: int
    fecha_ingreso: date
    ultimo_pago: Optional[date] = None
    activo: bool
    cuota_al_dia: bool

    class Config:
        from_attributes = True
