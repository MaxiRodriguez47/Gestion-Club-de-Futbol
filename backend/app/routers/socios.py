from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user, requiere_admin
from app.schemas.socio import SocioCreate, SocioUpdate, SocioOut, RegistrarPago
from app.crud import socio as crud_socio

router = APIRouter(prefix="/socios", tags=["Socios"])

@router.post("/", response_model=SocioOut, status_code=status.HTTP_201_CREATED)
def crear_socio(socio: SocioCreate, db: Session = Depends(get_db), admin_actual=Depends(requiere_admin)):
    if crud_socio.get_socio_por_dni(db, socio.dni):
        raise HTTPException(status_code=400, detail="Ya existe un socio con ese DNI")
    return crud_socio.crear_socio(db, socio)

@router.get("/", response_model=List[SocioOut])
def listar_socios(
    skip: int = 0,
    limit: int = 100,
    solo_activos: bool = True,
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_current_user)
):
    return crud_socio.get_socios(db, skip, limit, solo_activos)

@router.get("/morosos", response_model=List[SocioOut])
def listar_socios_morosos(db: Session = Depends(get_db), usuario_actual=Depends(get_current_user)):
    return crud_socio.get_socios_con_cuota_vencida(db)

@router.get("/{socio_id}", response_model=SocioOut)
def obtener_socio(socio_id: int, db: Session = Depends(get_db), usuario_actual=Depends(get_current_user)):
    db_socio = crud_socio.get_socio(db, socio_id)
    if not db_socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return db_socio

@router.put("/{socio_id}", response_model=SocioOut)
def actualizar_socio(socio_id: int, socio: SocioUpdate, db: Session = Depends(get_db), admin_actual=Depends(requiere_admin)):
    db_socio = crud_socio.actualizar_socio(db, socio_id, socio)
    if not db_socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return db_socio

@router.patch("/{socio_id}/pagar-cuota", response_model=SocioOut)
def registrar_pago(socio_id: int, pago: RegistrarPago, db: Session = Depends(get_db), admin_actual=Depends(requiere_admin)):
    db_socio = crud_socio.registrar_pago(db, socio_id, pago.fecha_pago)
    if not db_socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return db_socio

@router.delete("/{socio_id}", response_model=SocioOut)
def dar_de_baja_socio(socio_id: int, db: Session = Depends(get_db), admin_actual=Depends(requiere_admin)):
    db_socio = crud_socio.eliminar_socio(db, socio_id)
    if not db_socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return db_socio
