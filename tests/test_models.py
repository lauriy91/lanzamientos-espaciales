import pytest
from datetime import datetime
from web.models.lanzamiento import LanzamientoBase, LanzamientoCrear, Lanzamiento
from web.models.modelos_sql import ModeloLanzamiento

def test_lanzamiento_base():
    """Test para verificar la creación de un LanzamientoBase"""
    lanzamiento = LanzamientoBase(
        nombre_mision="Misión de Prueba",
        fecha_lanzamiento=datetime.utcnow(),
        nombre_cohete="Falcon 9",
        sitio_lanzamiento="Centro Espacial Kennedy",
        lanzamiento_exitoso=True
    )
    
    assert lanzamiento.nombre_mision == "Misión de Prueba"
    assert isinstance(lanzamiento.fecha_lanzamiento, datetime)
    assert lanzamiento.nombre_cohete == "Falcon 9"
    assert lanzamiento.sitio_lanzamiento == "Centro Espacial Kennedy"
    assert lanzamiento.lanzamiento_exitoso == True
    assert lanzamiento.proximo == False
    assert lanzamiento.detalles is None
    assert lanzamiento.enlaces is None

def test_lanzamiento_crear():
    """Test para verificar la creación de un LanzamientoCrear"""
    lanzamiento = LanzamientoCrear(
        id_lanzamiento="prueba-123",
        nombre_mision="Misión de Prueba",
        fecha_lanzamiento=datetime.utcnow(),
        nombre_cohete="Falcon 9",
        sitio_lanzamiento="Centro Espacial Kennedy",
        lanzamiento_exitoso=True
    )
    
    assert lanzamiento.id_lanzamiento == "prueba-123"
    assert lanzamiento.nombre_mision == "Misión de Prueba"

def test_lanzamiento():
    """Test para verificar la creación de un Lanzamiento"""
    lanzamiento = Lanzamiento(
        id_lanzamiento="prueba-123",
        nombre_mision="Misión de Prueba",
        fecha_lanzamiento=datetime.utcnow(),
        nombre_cohete="Falcon 9",
        sitio_lanzamiento="Centro Espacial Kennedy",
        lanzamiento_exitoso=True
    )
    
    assert lanzamiento.id_lanzamiento == "prueba-123"
    assert isinstance(lanzamiento.fecha_creacion, datetime)
    assert isinstance(lanzamiento.fecha_actualizacion, datetime)

def test_lanzamiento_validacion():
    """Test para verificar la validación de campos requeridos"""
    with pytest.raises(ValueError):
        LanzamientoBase(
            # Falta nombre_mision
            fecha_lanzamiento=datetime.utcnow(),
            nombre_cohete="Falcon 9",
            sitio_lanzamiento="Centro Espacial Kennedy",
            lanzamiento_exitoso=True
        )

def test_modelo_lanzamiento(db_prueba):
    """Test para el modelo SQLAlchemy"""
    datos_lanzamiento = {
        "id_lanzamiento": "prueba-1",
        "nombre_mision": "Misión de Prueba",
        "fecha_lanzamiento": datetime.utcnow(),
        "nombre_cohete": "Cohete de Prueba",
        "sitio_lanzamiento": "Sitio de Prueba",
        "lanzamiento_exitoso": True,
        "proximo": True,
        "detalles": "Detalles de prueba",
        "enlaces": {"webcast": "https://prueba.com"}
    }
    
    # Crear modelo
    lanzamiento = ModeloLanzamiento.desde_dict(datos_lanzamiento)
    db_prueba.add(lanzamiento)
    db_prueba.commit()
    
    # Recuperar modelo
    lanzamiento_guardado = db_prueba.query(ModeloLanzamiento).filter_by(id_lanzamiento=datos_lanzamiento["id_lanzamiento"]).first()
    assert lanzamiento_guardado is not None
    assert lanzamiento_guardado.nombre_mision == datos_lanzamiento["nombre_mision"]
    assert lanzamiento_guardado.nombre_cohete == datos_lanzamiento["nombre_cohete"]
    
    # Verificar conversión a diccionario
    lanzamiento_dict = lanzamiento_guardado.a_dict()
    assert lanzamiento_dict["id_lanzamiento"] == datos_lanzamiento["id_lanzamiento"]
    assert lanzamiento_dict["nombre_mision"] == datos_lanzamiento["nombre_mision"] 