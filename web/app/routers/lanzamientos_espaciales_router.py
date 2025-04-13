from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ...database.config import obtener_db
from ..services.lanzamientos_espaciales_service import LanzamientosEspacialesService
from ...models.lanzamiento import Lanzamiento

router = APIRouter(
    prefix="/lanzamientos",
    tags=["Lanzamientos"],
    responses={404: {"description": "No encontrado"}},
)
lanzamientos_service = LanzamientosEspacialesService()


@router.post(
    "/sincronizar",
    response_model=Dict[str, Any],
    description="Sincroniza los datos con la API de SpaceX",
)
async def sincronizar_datos(db: Session = Depends(obtener_db)):
    return await lanzamientos_service.sincronizar_datos_services(db)


@router.get(
    "/",
    response_model=List[Lanzamiento],
    description="Obtener todos los lanzamientos",
)
async def get_lanzamientos(db: Session = Depends(obtener_db)):
    return await lanzamientos_service.get_lanzamientos_services(db)


@router.get(
    "/{id_lanzamiento}",
    response_model=Lanzamiento,
    description="Obtener lanzamiento por ID.",
)
async def get_lanzamiento_id(id_lanzamiento: str, db: Session = Depends(obtener_db)):
    return await lanzamientos_service.get_lanzamiento_id_services(db, id_lanzamiento)


@router.get(
    "/lanzamientos_proximos/proximos",
    response_model=List[Lanzamiento],
    description="Obtener los próximos lanzamientos programados.",
)
async def get_proximos_lanzamientos(db: Session = Depends(obtener_db)):
    return await lanzamientos_service.get_proximos_lanzamientos_services(db)


@router.get(
    "/lanzamientos_pasados/pasados",
    response_model=List[Lanzamiento],
    description="Obtener los lanzamientos pasados.",
)
async def get_lanzamientos_pasados(db: Session = Depends(obtener_db)):
    return await lanzamientos_service.get_lanzamientos_pasados_services(db)


@router.get(
    "/estadisticas/cohetes",
    response_model=Dict[str, Any],
    description="Obtener estadísticas de lanzamientos por cohete.",
)
async def get_estadisticas_cohetes(db: Session = Depends(obtener_db)):
    return await lanzamientos_service.get_estadisticas_cohetes_services(db)


@router.get(
    "/estadisticas/estado",
    response_model=Dict[str, Any],
    description="Obtener estadísticas de lanzamientos por estado.",
)
async def get_estadisticas_estado(db: Session = Depends(obtener_db)):
    return await lanzamientos_service.get_estadisticas_estado_services(db)
