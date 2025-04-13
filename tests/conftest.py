import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import os
from datetime import datetime

from web.database.config import Base, get_db
from web.main import app
from web.models.modelos_sql import ModeloLanzamiento

# Configuración de la base de datos de prueba
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/spacex_test"

@pytest.fixture(scope="session")
def motor_prueba():
    """Crear motor de base de datos de prueba"""
    motor = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=motor)
    yield motor
    Base.metadata.drop_all(bind=motor)

@pytest.fixture(scope="function")
def db_prueba(motor_prueba):
    """Crear sesión de base de datos de prueba"""
    SesionLocalPrueba = sessionmaker(autocommit=False, autoflush=False, bind=motor_prueba)
    db = SesionLocalPrueba()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def cliente(db_prueba):
    """Crear cliente de prueba FastAPI"""
    def override_get_db():
        try:
            yield db_prueba
        finally:
            db_prueba.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as cliente_prueba:
        yield cliente_prueba
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def lanzamiento_muestra():
    """Crear un lanzamiento de muestra para pruebas"""
    return {
        "id_lanzamiento": "prueba-lanzamiento-1",
        "nombre_mision": "Misión de Prueba",
        "fecha_lanzamiento": datetime.utcnow(),
        "nombre_cohete": "Cohete de Prueba",
        "sitio_lanzamiento": "Sitio de Prueba",
        "lanzamiento_exitoso": True,
        "proximo": True,
        "detalles": "Detalles del lanzamiento de prueba",
        "enlaces": {"webcast": "https://prueba.com"}
    }

@pytest.fixture(scope="function")
def lanzamiento_db(db_prueba, lanzamiento_muestra):
    """Crear un lanzamiento en la base de datos de prueba"""
    lanzamiento = ModeloLanzamiento.desde_dict(lanzamiento_muestra)
    db_prueba.add(lanzamiento)
    db_prueba.commit()
    db_prueba.refresh(lanzamiento)
    return lanzamiento 