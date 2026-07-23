from sqlalchemy.orm import Session
from app.models.jugador import Jugador
from app.schemas.jugador import JugadorCreate, JugadorUpdate

def get_jugador(db: Session, jugador_id: int):
    return db.query(Jugador).filter(Jugador.id == jugador_id).first()

def get_jugador_por_numero(db: Session, numero: int):
    return db.query(Jugador).filter(Jugador.numero_camiseta == numero).first()

def get_jugadores(db: Session, skip: int = 0, limit: int = 100, categoria: str = None):
    query = db.query(Jugador)
    if categoria:
        query = query.filter(Jugador.categoria == categoria)
    return query.offset(skip).limit(limit).all()

def crear_jugador(db: Session, jugador: JugadorCreate):
    db_jugador = Jugador(**jugador.model_dump())
    db.add(db_jugador)
    db.commit()
    db.refresh(db_jugador)
    return db_jugador

def actualizar_jugador(db: Session, jugador_id: int, jugador: JugadorUpdate):
    db_jugador = get_jugador(db, jugador_id)
    if not db_jugador:
        return None
    datos = jugador.model_dump(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(db_jugador, campo, valor)
    db.commit()
    db.refresh(db_jugador)
    return db_jugador

def eliminar_jugador(db: Session, jugador_id: int):
    db_jugador = get_jugador(db, jugador_id)
    if not db_jugador:
        return None
    db.delete(db_jugador)
    db.commit()
    return db_jugador