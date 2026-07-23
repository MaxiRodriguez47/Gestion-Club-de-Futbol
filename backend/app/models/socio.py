from sqlalchemy import Column, Integer, String, Date, Boolean, Float
from datetime import date, timedelta
from app.database import Base

DIAS_GRACIA = 30  # días de margen tras el vencimiento antes de considerar cuota vencida

class Socio(Base):
    __tablename__ = "socios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(100), nullable=False, index=True)
    dni = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(100), nullable=True)
    telefono = Column(String(30), nullable=True)
    fecha_ingreso = Column(Date, nullable=False)
    categoria_socio = Column(String(50), default="General")  # General, Vitalicio, Cadete
    ultimo_pago = Column(Date, nullable=True)
    monto_cuota = Column(Float, default=0.0)
    activo = Column(Boolean, default=True)  # socio dado de baja del club

    @property
    def cuota_al_dia(self) -> bool:
        if self.ultimo_pago is None:
            return False
        return date.today() <= self.ultimo_pago + timedelta(days=DIAS_GRACIA)