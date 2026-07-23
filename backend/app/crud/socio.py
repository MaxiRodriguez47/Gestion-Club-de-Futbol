from sqlalchemy.orm import Session
from datetime import date
from app.models.socio import Socio
from app.schemas.socio import SocioCreate, SocioUpdate

def get_socio(db: Session, socio_id: int):
    return db.query(Socio).filter(Socio.id == socio_id).first()

def get_socio_por_dni(db: Session, dni: str):
    return db.query(Socio).filter(Socio.dni == dni).first()

def get_socios(db: Session, skip: int = 0, limit: int = 100, solo_activos: bool = True):
    query = db.query(Socio)
    if solo_activos:
        query = query.filter(Socio.activo == True)
    return query.offset(skip).limit(limit).all()

def get_socios_con_cuota_vencida(db: Session):
    """Trae todos y filtra en Python, porque cuota_al_dia es calculada, no una columna SQL."""
    todos = db.query(Socio).filter(Socio.activo == True).all()
    return [s for s in todos if not s.cuota_al_dia]

def crear_socio(db: Session, socio: SocioCreate):
    db_socio = Socio(**socio.model_dump())
    db.add(db_socio)
    db.commit()
    db.refresh(db_socio)
    return db_socio

def actualizar_socio(db: Session, socio_id: int, socio: SocioUpdate):
    db_socio = get_socio(db, socio_id)
    if not db_socio:
        return None
    datos = socio.model_dump(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(db_socio, campo, valor)
    db.commit()
    db.refresh(db_socio)
    return db_socio

def registrar_pago(db: Session, socio_id: int, fecha_pago: date):
    db_socio = get_socio(db, socio_id)
    if not db_socio:
        return None
    db_socio.ultimo_pago = fecha_pago
    db.commit()
    db.refresh(db_socio)
    return db_socio

def eliminar_socio(db: Session, socio_id: int):
    """Baja lógica, no borrado físico: nunca perdés el historial del socio."""
    db_socio = get_socio(db, socio_id)
    if not db_socio:
        return None
    db_socio.activo = False
    db.commit()
    db.refresh(db_socio)
    return db_socio