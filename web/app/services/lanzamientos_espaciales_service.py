from typing import List, Dict, Any
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ...database.repositorio import obtener_repositorio
from ...services.spacex_service import ServicioSpaceX


class LanzamientosEspacialesService:
    def __init__(self):
        pass

    async def get_lanzamientos_services(self, db: Session) -> List[Dict[str, Any]]:
        try:
            repositorio = obtener_repositorio(db)
            return repositorio.obtener_todos_lanzamientos()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_lanzamiento_id_services(
        self, db: Session, id_lanzamiento: str
    ) -> Dict[str, Any]:
        try:
            repositorio = obtener_repositorio(db)
            lanzamiento = repositorio.obtener_lanzamiento_por_id(id_lanzamiento)
            if not lanzamiento:
                raise HTTPException(status_code=404, detail="Lanzamiento no encontrado")
            return lanzamiento
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_estadisticas_cohetes_services(self, db: Session) -> Dict[str, Any]:
        try:
            repositorio = obtener_repositorio(db)
            lanzamientos = repositorio.obtener_todos_lanzamientos()

            stats = {}
            for lanzamiento in lanzamientos:
                cohete = lanzamiento["nombre_cohete"]
                if cohete not in stats:
                    stats[cohete] = {"total": 0, "exitosos": 0, "fallidos": 0}
                stats[cohete]["total"] += 1
                if lanzamiento["lanzamiento_exitoso"]:
                    stats[cohete]["exitosos"] += 1
                else:
                    stats[cohete]["fallidos"] += 1

            return stats
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_estadisticas_estado_services(self, db: Session) -> Dict[str, Any]:
        try:
            repositorio = obtener_repositorio(db)
            lanzamientos = repositorio.obtener_todos_lanzamientos()

            stats = {
                "total": len(lanzamientos),
                "exitosos": 0,
                "fallidos": 0,
                "proximos": 0,
            }

            for lanzamiento in lanzamientos:
                if lanzamiento["lanzamiento_exitoso"]:
                    stats["exitosos"] += 1
                elif not lanzamiento["proximo"]:
                    stats["fallidos"] += 1
                if lanzamiento["proximo"]:
                    stats["proximos"] += 1

            return stats
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_proximos_lanzamientos_services(
        self, db: Session
    ) -> List[Dict[str, Any]]:
        try:
            repositorio = obtener_repositorio(db)
            return repositorio.obtener_proximos_lanzamientos()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_lanzamientos_pasados_services(
        self, db: Session
    ) -> List[Dict[str, Any]]:
        try:
            repositorio = obtener_repositorio(db)
            return repositorio.obtener_lanzamientos_pasados()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def sincronizar_datos_services(self, db: Session) -> Dict[str, Any]:
        try:
            # Obtener datos de la API
            lanzamientos_api = ServicioSpaceX.obtener_lanzamientos()

            # Convertir y guardar cada lanzamiento
            for datos_lanzamiento in lanzamientos_api:
                modelo = ServicioSpaceX.convertir_a_modelo(datos_lanzamiento)
                db.merge(modelo)

            db.commit()
            return {
                "mensaje": f"Se sincronizaron {len(lanzamientos_api)} lanzamientos exitosamente"
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Error al sincronizar datos: {str(e)}"
            )
