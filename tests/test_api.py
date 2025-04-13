from fastapi.testclient import TestClient
from web.main import app
import pytest
from datetime import datetime

cliente = TestClient(app)

def test_leer_raiz(cliente):
    """Test para el endpoint raíz"""
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    assert "mensaje" in respuesta.json()
    assert "documentacion" in respuesta.json()

def test_obtener_lanzamientos_vacio(cliente):
    """Test para obtener lanzamientos cuando la base de datos está vacía"""
    respuesta = cliente.get("/lanzamientos")
    assert respuesta.status_code == 200
    assert respuesta.json() == []

def test_obtener_lanzamientos(cliente, lanzamiento_db):
    """Test para obtener todos los lanzamientos"""
    respuesta = cliente.get("/lanzamientos")
    assert respuesta.status_code == 200
    lanzamientos = respuesta.json()
    assert len(lanzamientos) == 1
    assert lanzamientos[0]["id_lanzamiento"] == lanzamiento_db.id_lanzamiento

def test_obtener_lanzamiento_por_id(cliente, lanzamiento_db):
    """Test para obtener un lanzamiento por ID"""
    respuesta = cliente.get(f"/lanzamientos/{lanzamiento_db.id_lanzamiento}")
    assert respuesta.status_code == 200
    lanzamiento = respuesta.json()
    assert lanzamiento["id_lanzamiento"] == lanzamiento_db.id_lanzamiento
    assert lanzamiento["nombre_mision"] == lanzamiento_db.nombre_mision

def test_obtener_lanzamiento_por_id_no_existe(cliente):
    """Test para obtener un lanzamiento que no existe"""
    respuesta = cliente.get("/lanzamientos/no-existe")
    assert respuesta.status_code == 404
    assert "detalle" in respuesta.json()

def test_obtener_proximos_lanzamientos(cliente, lanzamiento_db):
    """Test para obtener lanzamientos próximos"""
    respuesta = cliente.get("/lanzamientos/proximos")
    assert respuesta.status_code == 200
    lanzamientos = respuesta.json()
    assert len(lanzamientos) == 1
    assert lanzamientos[0]["id_lanzamiento"] == lanzamiento_db.id_lanzamiento

def test_obtener_lanzamientos_pasados(cliente, db_prueba, lanzamiento_db):
    """Test para obtener lanzamientos pasados"""
    # Modificar el lanzamiento existente para que sea pasado
    lanzamiento_db.proximo = False
    db_prueba.commit()
    
    respuesta = cliente.get("/lanzamientos/pasados")
    assert respuesta.status_code == 200
    lanzamientos = respuesta.json()
    assert len(lanzamientos) == 1
    assert lanzamientos[0]["id_lanzamiento"] == lanzamiento_db.id_lanzamiento

def test_get_lanzamientos_vacios(cliente):
    """Test para obtener lanzamientos cuando la base de datos está vacía"""
    response = cliente.get("/launches")
    assert response.status_code == 200
    assert response.json() == []

def test_get_lanzamientos(cliente, db_launch):
    """Test para obtener todos los lanzamientos"""
    response = cliente.get("/launches")
    assert response.status_code == 200
    launches = response.json()
    assert len(launches) == 1
    assert launches[0]["id_lanzamiento"] == db_launch.id_lanzamiento

def test_get_lanzamientos_id(cliente, db_launch):
    """Test para obtener un lanzamiento por ID"""
    response = cliente.get(f"/launches/{db_launch.id_lanzamiento}")
    assert response.status_code == 200
    launch = response.json()
    assert launch["id_lanzamiento"] == db_launch.id_lanzamiento
    assert launch["mission_name"] == db_launch.mission_name

def test_get_lanzamientos_id_no_existe(cliente):
    """Test para obtener un lanzamiento que no existe"""
    response = cliente.get("/launches/non-existent")
    assert response.status_code == 404
    assert "detail" in response.json()

def test_get_proximos_lanzamientos(cliente, db_launch):
    """Test para obtener lanzamientos próximos"""
    response = cliente.get("/launches/upcoming")
    assert response.status_code == 200
    launches = response.json()
    assert len(launches) == 1
    assert launches[0]["id_lanzamiento"] == db_launch.id_lanzamiento

def test_get_lanzamientos_pasados(cliente, test_db, db_launch):
    """Test para obtener lanzamientos pasados"""
    # Modificar el lanzamiento existente para que sea pasado
    db_launch.upcoming = False
    test_db.commit()
    
    response = cliente.get("/launches/past")
    assert response.status_code == 200
    launches = response.json()
    assert len(launches) == 1
    assert launches[0]["id_lanzamiento"] == db_launch.id_lanzamiento

def test_obtener_lanzamientos():
    """Test para obtener todos los lanzamientos"""
    response = cliente.get("/lanzamientos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obtener_lanzamiento_por_id():
    """Test para obtener un lanzamiento específico"""
    response = cliente.get("/lanzamientos")
    assert response.status_code == 200
    lanzamientos = response.json()
    
    if lanzamientos:
        id_lanzamiento = lanzamientos[0]["id_lanzamiento"]
        response = cliente.get(f"/lanzamientos/{id_lanzamiento}")
        assert response.status_code == 200
        lanzamiento = response.json()
        assert lanzamiento["id_lanzamiento"] == id_lanzamiento
    else:
        # Si no hay lanzamientos, probamos con un ID que no existe
        response = cliente.get("/lanzamientos/no-existe")
        assert response.status_code == 404

def test_obtener_proximos_lanzamientos():
    """Test para obtener los próximos lanzamientos"""
    response = cliente.get("/lanzamientos/proximos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for lanzamiento in response.json():
        assert lanzamiento["proximo"] == True

def test_obtener_lanzamientos_pasados():
    """Test para obtener los lanzamientos pasados"""
    response = cliente.get("/lanzamientos/pasados")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for lanzamiento in response.json():
        assert lanzamiento["proximo"] == False 