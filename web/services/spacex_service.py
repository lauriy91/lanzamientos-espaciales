import requests
from datetime import datetime, timezone
from typing import List, Dict, Any
from ..models.modelos_sql import ModeloLanzamiento

class ServicioSpaceX:
    BASE_URL = "https://api.spacexdata.com/v4"

    @classmethod
    def obtener_lanzamientos(cls) -> List[Dict[str, Any]]:
        response = requests.get(f"{cls.BASE_URL}/launches")
        response.raise_for_status()
        return response.json()

    @classmethod
    def obtener_proximo_lanzamiento(cls) -> Dict[str, Any]:
        response = requests.get(f"{cls.BASE_URL}/launches/next")
        response.raise_for_status()
        return response.json()

    @classmethod
    def obtener_lanzamiento_por_id(cls, id_lanzamiento: str) -> Dict[str, Any]:
        response = requests.get(f"{cls.BASE_URL}/launches/{id_lanzamiento}")
        response.raise_for_status()
        return response.json()

    @classmethod
    def convertir_a_modelo(cls, datos_api: Dict[str, Any]) -> ModeloLanzamiento:
        fecha_lanzamiento = datetime.fromisoformat(datos_api['date_utc'].replace('Z', '+00:00'))
        fecha_actual = datetime.now(timezone.utc)
        
        lanzamiento_exitoso = False
        if datos_api.get('success') is not None:
            lanzamiento_exitoso = datos_api['success']
        elif datos_api.get('upcoming') is not None:
            lanzamiento_exitoso = not datos_api['upcoming']
        
        proximo = datos_api.get('upcoming', False)
        if not proximo:
            proximo = fecha_lanzamiento > fecha_actual
        
        return ModeloLanzamiento(
            id_lanzamiento=datos_api['id'],
            nombre_mision=datos_api['name'],
            fecha_lanzamiento=fecha_lanzamiento,
            nombre_cohete=datos_api['rocket'],
            sitio_lanzamiento=datos_api['launchpad'],
            lanzamiento_exitoso=lanzamiento_exitoso,
            proximo=proximo,
            detalles=datos_api.get('details', ''),
            enlaces={
                'patch': datos_api.get('links', {}).get('patch', {}).get('small'),
                'webcast': datos_api.get('links', {}).get('webcast'),
                'article': datos_api.get('links', {}).get('article'),
                'wikipedia': datos_api.get('links', {}).get('wikipedia')
            }
        ) 