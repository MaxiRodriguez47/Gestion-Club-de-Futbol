from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies import get_db
from app.schemas.jugador import JugadorCreate, JugadorUpdate, JugadorOut
from app.crud import jugador as crud_jugador

router = APIRouter(prefix="/jugadores", tags=["Jugadores"])

@router.post("/", response_model=JugadorOut, status_code=status.HTTP_201_CREATED)
def crear_jugador(jugador: JugadorCreate, db: Session = Depends(get_db)):
    existente = crud_jugador.get_jugador_por_numero(db, jugador.numero_camiseta)
    if existente:
        raise HTTPException(
            status_code=400,
            detail=f"El dorsal #{jugador.numero_camiseta} ya está asignado."
        )
    return crud_jugador.crear_jugador(db, jugador)

@router.get("/", response_model=List[JugadorOut])
def listar_jugadores(
    skip: int = 0,
    limit: int = 100,
    categoria: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud_jugador.get_jugadores(db, skip, limit, categoria)

@router.get("/{jugador_id}", response_model=JugadorOut)
def obtener_jugador(jugador_id: int, db: Session = Depends(get_db)):
    db_jugador = crud_jugador.get_jugador(db, jugador_id)
    if not db_jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return db_jugador

@router.put("/{jugador_id}", response_model=JugadorOut)
def actualizar_jugador(jugador_id: int, jugador: JugadorUpdate, db: Session = Depends(get_db)):
    db_jugador = crud_jugador.actualizar_jugador(db, jugador_id, jugador)
    if not db_jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return db_jugador

@router.delete("/{jugador_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_jugador(jugador_id: int, db: Session = Depends(get_db)):
    db_jugador = crud_jugador.eliminar_jugador(db, jugador_id)
    if not db_jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")