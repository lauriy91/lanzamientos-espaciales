from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from .database.config import obtener_db, init_db
from .database.repositorio import obtener_repositorio
from .models.lanzamiento import Lanzamiento, LanzamientoCrear

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="API de Lanzamientos SpaceX",
    description="API para obtener información sobre lanzamientos de SpaceX",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Inicializar la base de datos
@app.on_event("startup")
async def evento_inicio():
    init_db()


@app.get(
    "/",
    tags=["Inicio"],
    description="Endpoint raíz que proporciona información básica sobre la API.",
)
async def inicio():
    return {
        "mensaje": "Bienvenido a la API de Lanzamientos de SpaceX",
        "documentacion": "/docs",
        "redoc": "/redoc",
    }


@app.get(
    "/lanzamientos",
    response_model=List[Lanzamiento],
    tags=["Lanzamientos"],
    description="Obtener todos los lanzamientos.",
)
async def obtener_lanzamientos(db: Session = Depends(obtener_db)):
    repositorio = obtener_repositorio(db)
    return repositorio.obtener_todos_lanzamientos()


@app.get(
    "/lanzamientos/{id_lanzamiento}",
    response_model=Lanzamiento,
    tags=["Lanzamientos"],
    description="Obtener un lanzamiento específico por su ID.",
)
async def obtener_lanzamiento(id_lanzamiento: str, db: Session = Depends(obtener_db)):
    repositorio = obtener_repositorio(db)
    lanzamiento = repositorio.obtener_lanzamiento_por_id(id_lanzamiento)
    if not lanzamiento:
        raise HTTPException(status_code=404, detail="Lanzamiento no encontrado")
    return lanzamiento


@app.get(
    "/lanzamientos/proximos",
    response_model=List[Lanzamiento],
    tags=["Lanzamientos"],
    description="Obtener los próximos lanzamientos.",
)
async def obtener_proximos_lanzamientos(db: Session = Depends(obtener_db)):
    repositorio = obtener_repositorio(db)
    return repositorio.obtener_proximos_lanzamientos()


@app.get(
    "/lanzamientos/pasados",
    response_model=List[Lanzamiento],
    tags=["Lanzamientos"],
    description="Obtener los lanzamientos pasados.",
)
async def obtener_lanzamientos_pasados(db: Session = Depends(obtener_db)):
    repositorio = obtener_repositorio(db)
    return repositorio.obtener_lanzamientos_pasados()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
