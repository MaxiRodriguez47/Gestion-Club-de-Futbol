from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class PosicionEnum(str, enum.Enum):
    ARQUERO = "Arquero"
    DEFENSOR = "Defensor"
    MEDIOCAMPISTA = "Mediocampista"
    DELANTERO = "Delantero"

class CategoriaEnum(str, enum.Enum):
    PRIMERA = "Primera"
    RESERVA = "Reserva"
    SUB_20 = "Sub-20"
    SUB_17 = "Sub-17"
    SUB_15 = "Sub-15"

class Jugador(Base):
    __tablename__ = "jugadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(100), nullable=False, index=True)
    posicion = Column(Enum(PosicionEnum), nullable=False)
    numero_camiseta = Column(Integer, unique=True, nullable=False)
    categoria = Column(Enum(CategoriaEnum), nullable=False)
    fecha_nacimiento = Column(String, nullable=True)  # se puede pasar a Date
    activo = Column(Integer, default=1)  # 1=activo, 0=dado de baja

    estadisticas = relationship("EstadisticaPartido", back_populates="jugador")