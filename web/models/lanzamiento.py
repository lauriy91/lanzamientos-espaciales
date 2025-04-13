from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class LanzamientoBase(BaseModel):
    nombre_mision: str
    fecha_lanzamiento: datetime
    nombre_cohete: str
    sitio_lanzamiento: str
    lanzamiento_exitoso: bool
    proximo: bool = False
    detalles: Optional[str] = None
    enlaces: Optional[Dict[str, Any]] = None

class LanzamientoCrear(LanzamientoBase):
    id_lanzamiento: str

class Lanzamiento(LanzamientoBase):
    id_lanzamiento: str
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 