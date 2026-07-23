from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey
import enum
from app.database import Base

class RolEnum(str, enum.Enum):
    ADMIN = "admin"
    SOCIO = "socio"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    rol = Column(Enum(RolEnum), nullable=False, default=RolEnum.SOCIO)
    activo = Column(Boolean, default=True)
    socio_id = Column(Integer, ForeignKey("socios.id"), nullable=True)
