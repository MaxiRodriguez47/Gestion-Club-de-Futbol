from sqlalchemy.orm import Session
from app.models.partido import Partido
from app.schemas.partido import PartidoCreate, PartidoUpdate, RegistrarResultado

def get_partido(db: Session, partido_id: int):
    return db.query(Partido).filter(Partido.id == partido_id).first()

def get_partidos(db: Session, skip: int = 0, limit: int = 100, solo_pendientes: bool = False):
    query = db.query(Partido).order_by(Partido.fecha)
    if solo_pendientes:
        query = query.filter(Partido.jugado == 0)
    return query.offset(skip).limit(limit).all()

def crear_partido(db: Session, partido: PartidoCreate):
    db_partido = Partido(**partido.model_dump())
    db.add(db_partido)
    db.commit()
    db.refresh(db_partido)
    return db_partido

def crear_fixture(db: Session, partidos: list[PartidoCreate]):
    """Carga varios partidos de una sola vez, útil para armar el fixture completo al inicio de temporada."""
    db_partidos = [Partido(**p.model_dump()) for p in partidos]
    db.add_all(db_partidos)
    db.commit()
    for p in db_partidos:
        db.refresh(p)
    return db_partidos

def actualizar_partido(db: Session, partido_id: int, partido: PartidoUpdate):
    db_partido = get_partido(db, partido_id)
    if not db_partido:
        return None
    datos = partido.model_dump(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(db_partido, campo, valor)
    db.commit()
    db.refresh(db_partido)
    return db_partido

def registrar_resultado(db: Session, partido_id: int, resultado: RegistrarResultado):
    db_partido = get_partido(db, partido_id)
    if not db_partido:
        return None
    db_partido.goles_favor = resultado.goles_favor
    db_partido.goles_contra = resultado.goles_contra
    db_partido.jugado = 1
    db.commit()
    db.refresh(db_partido)
    return db_partido

def eliminar_partido(db: Session, partido_id: int):
    db_partido = get_partido(db, partido_id)
    if not db_partido:
        return None
    db.delete(db_partido)
    db.commit()
    return db_partido