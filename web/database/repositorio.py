from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import boto3
from .config import obtener_tabla_dynamodb, es_desarrollo
from ..models.modelos_sql import ModeloLanzamiento

class RepositorioLanzamientos(ABC):
    @abstractmethod
    def obtener_todos_lanzamientos(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def obtener_lanzamiento_por_id(self, id_lanzamiento: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def obtener_proximos_lanzamientos(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def obtener_lanzamientos_pasados(self) -> List[Dict[str, Any]]:
        pass

class RepositorioPostgresLanzamientos(RepositorioLanzamientos):
    def __init__(self, db: Session):
        self.db = db

    def obtener_todos_lanzamientos(self) -> List[Dict[str, Any]]:
        lanzamientos = self.db.query(ModeloLanzamiento).all()
        return [lanzamiento.a_dict() for lanzamiento in lanzamientos]

    def obtener_lanzamiento_por_id(self, id_lanzamiento: str) -> Optional[Dict[str, Any]]:
        lanzamiento = self.db.query(ModeloLanzamiento).filter(ModeloLanzamiento.id_lanzamiento == id_lanzamiento).first()
        return lanzamiento.a_dict() if lanzamiento else None

    def obtener_proximos_lanzamientos(self) -> List[Dict[str, Any]]:
        lanzamientos = self.db.query(ModeloLanzamiento).filter(ModeloLanzamiento.proximo == True).all()
        return [lanzamiento.a_dict() for lanzamiento in lanzamientos]

    def obtener_lanzamientos_pasados(self) -> List[Dict[str, Any]]:
        lanzamientos = self.db.query(ModeloLanzamiento).filter(ModeloLanzamiento.proximo == False).all()
        return [lanzamiento.a_dict() for lanzamiento in lanzamientos]

class RepositorioDynamoDBLanzamientos(RepositorioLanzamientos):
    def __init__(self):
        self.tabla = obtener_tabla_dynamodb()

    def obtener_todos_lanzamientos(self) -> List[Dict[str, Any]]:
        respuesta = self.tabla.scan()
        return respuesta.get('Items', [])

    def obtener_lanzamiento_por_id(self, id_lanzamiento: str) -> Optional[Dict[str, Any]]:
        respuesta = self.tabla.get_item(Key={'id_lanzamiento': id_lanzamiento})
        return respuesta.get('Item')

    def obtener_proximos_lanzamientos(self) -> List[Dict[str, Any]]:
        respuesta = self.tabla.scan(
            FilterExpression='proximo = :proximo',
            ExpressionAttributeValues={':proximo': True}
        )
        return respuesta.get('Items', [])

    def obtener_lanzamientos_pasados(self) -> List[Dict[str, Any]]:
        respuesta = self.tabla.scan(
            FilterExpression='proximo = :proximo',
            ExpressionAttributeValues={':proximo': False}
        )
        return respuesta.get('Items', [])

def obtener_repositorio(db: Session = None) -> RepositorioLanzamientos:
    """
    Función factory para obtener el repositorio apropiado basado en el entorno
    """
    if es_desarrollo():
        return RepositorioPostgresLanzamientos(db)
    return RepositorioDynamoDBLanzamientos() 