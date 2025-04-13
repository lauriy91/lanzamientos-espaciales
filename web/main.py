from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from .database.init_db import inicializar_base_datos
from .app.routers.lanzamientos_espaciales_router import router as lanzamientos_router

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    inicializar_base_datos()


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


app.include_router(lanzamientos_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
