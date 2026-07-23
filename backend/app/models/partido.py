from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class CondicionEnum(str, enum.Enum):
    LOCAL = "Local"
    VISITANTE = "Visitante"

class Partido(Base):
    __tablename__ = "partidos"

    id = Column(Integer, primary_key=True, index=True)
    rival = Column(String(100), nullable=False)
    fecha = Column(DateTime, nullable=False)
    condicion = Column(Enum(CondicionEnum), nullable=False)
    torneo = Column(String(100), nullable=True)
    goles_favor = Column(Integer, nullable=True)
    goles_contra = Column(Integer, nullable=True)
    jugado = Column(Integer, default=0)  # 0=pendiente, 1=jugado

    estadisticas = relationship("EstadisticaPartido", back_populates="partido")

class EstadisticaPartido(Base):
    """Tabla intermedia: qué jugador participó en qué partido y con qué stats."""
    __tablename__ = "estadisticas_partido"

    id = Column(Integer, primary_key=True, index=True)
    partido_id = Column(Integer, ForeignKey("partidos.id"), nullable=False)
    jugador_id = Column(Integer, ForeignKey("jugadores.id"), nullable=False)
    goles = Column(Integer, default=0)
    tarjetas_amarillas = Column(Integer, default=0)
    tarjetas_rojas = Column(Integer, default=0)
    titular = Column(Integer, default=1)

    partido = relationship("Partido", back_populates="estadisticas")
    jugador = relationship("Jugador", back_populates="estadisticas")