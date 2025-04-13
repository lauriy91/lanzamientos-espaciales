from sqlalchemy import Column, String, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from ..database.config import Base

class ModeloLanzamiento(Base):
    __tablename__ = "lanzamientos"

    id_lanzamiento = Column(String, primary_key=True, index=True)
    nombre_mision = Column(String)
    fecha_lanzamiento = Column(DateTime)
    nombre_cohete = Column(String)
    sitio_lanzamiento = Column(String)
    lanzamiento_exitoso = Column(Boolean)
    proximo = Column(Boolean, default=False)
    detalles = Column(String, nullable=True)
    enlaces = Column(JSON, nullable=True)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def a_dict(self):
        """Convertir el modelo a diccionario"""
        return {
            "id_lanzamiento": self.id_lanzamiento,
            "nombre_mision": self.nombre_mision,
            "fecha_lanzamiento": self.fecha_lanzamiento,
            "nombre_cohete": self.nombre_cohete,
            "sitio_lanzamiento": self.sitio_lanzamiento,
            "lanzamiento_exitoso": self.lanzamiento_exitoso,
            "proximo": self.proximo,
            "detalles": self.detalles,
            "enlaces": self.enlaces,
            "fecha_creacion": self.fecha_creacion,
            "fecha_actualizacion": self.fecha_actualizacion
        }

    @classmethod
    def desde_dict(cls, datos: dict):
        return cls(
            id_lanzamiento=datos.get("id_lanzamiento"),
            nombre_mision=datos.get("nombre_mision"),
            fecha_lanzamiento=datos.get("fecha_lanzamiento"),
            nombre_cohete=datos.get("nombre_cohete"),
            sitio_lanzamiento=datos.get("sitio_lanzamiento"),
            lanzamiento_exitoso=datos.get("lanzamiento_exitoso"),
            proximo=datos.get("proximo", False),
            detalles=datos.get("detalles"),
            enlaces=datos.get("enlaces")
        ) 