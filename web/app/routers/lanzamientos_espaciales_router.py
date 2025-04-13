from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from database_config.connection import get_db
from app.services.lanzamientos_espaciales_service import LanzamientosEspacialesService

router = APIRouter()
lanzamientos_service = LanzamientosEspacialesService()


@router.get(
    "/",
    response_model=List[Dict[str, Any]],
    description="Obtiener todos los lanzamientos",
)
async def get_lanzamientos(db: Any = Depends(get_db)):
    return await lanzamientos_service.get_all_launches(db)


@router.get(
    "/{launch_id}",
    response_model=Dict[str, Any],
    description="Obtiener lanzamiento por ID.",
)
async def get_lanzamiento(launch_id: str, db: Any = Depends(get_db)):
    return await lanzamientos_service.get_launch_by_id(db, launch_id)


@router.get(
    "/estadisticas/cohetes",
    response_model=Dict[str, Any],
    description="Obtiener estadísticas de lanzamientos por cohete.",
)
async def get_estadisticas_cohetes(db: Any = Depends(get_db)):
    return await lanzamientos_service.get_rocket_statistics(db)


@router.get(
    "/estadisticas/estado",
    response_model=Dict[str, Any],
    description="Obtiener estadísticas de lanzamientos por estado.",
)
async def get_estadisticas_estado(db: Any = Depends(get_db)):
    return await lanzamientos_service.get_launch_status_statistics(db)


@router.get(
    "/proximos",
    response_model=List[Dict[str, Any]],
    description="Obtiener los próximos lanzamientos programados.",
)
async def get_proximos_lanzamientos(db: Any = Depends(get_db)):
    return await lanzamientos_service.get_upcoming_launches(db)
