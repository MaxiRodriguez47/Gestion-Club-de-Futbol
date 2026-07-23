from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.schemas.partido import PartidoCreate, PartidoUpdate, PartidoOut, RegistrarResultado
from app.crud import partido as crud_partido

router = APIRouter(prefix="/partidos", tags=["Partidos"])

@router.post("/", response_model=PartidoOut, status_code=status.HTTP_201_CREATED)
def crear_partido(partido: PartidoCreate, db: Session = Depends(get_db)):
    return crud_partido.crear_partido(db, partido)

@router.post("/fixture", response_model=List[PartidoOut], status_code=status.HTTP_201_CREATED)
def cargar_fixture(partidos: List[PartidoCreate], db: Session = Depends(get_db)):
    """Carga el calendario completo de la temporada de una sola vez."""
    return crud_partido.crear_fixture(db, partidos)

@router.get("/", response_model=List[PartidoOut])
def listar_partidos(
    skip: int = 0,
    limit: int = 100,
    solo_pendientes: bool = False,
    db: Session = Depends(get_db)
):
    return crud_partido.get_partidos(db, skip, limit, solo_pendientes)

@router.get("/{partido_id}", response_model=PartidoOut)
def obtener_partido(partido_id: int, db: Session = Depends(get_db)):
    db_partido = crud_partido.get_partido(db, partido_id)
    if not db_partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return db_partido

@router.put("/{partido_id}", response_model=PartidoOut)
def actualizar_partido(partido_id: int, partido: PartidoUpdate, db: Session = Depends(get_db)):
    db_partido = crud_partido.actualizar_partido(db, partido_id, partido)
    if not db_partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return db_partido

@router.patch("/{partido_id}/resultado", response_model=PartidoOut)
def registrar_resultado(partido_id: int, resultado: RegistrarResultado, db: Session = Depends(get_db)):
    db_partido = crud_partido.registrar_resultado(db, partido_id, resultado)
    if not db_partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return db_partido

@router.delete("/{partido_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_partido(partido_id: int, db: Session = Depends(get_db)):
    db_partido = crud_partido.eliminar_partido(db, partido_id)
    if not db_partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")