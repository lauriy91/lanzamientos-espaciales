from fastapi import FastAPI
from app.routers import lanzamientos_espaciales_router
from database_config.connection import Base, get_engine

app = FastAPI(
    title="Lanzamientos Espaciales",
    description="API para seguimiento de lanzamientos espaciales de SpaceX",
    version="1.0.0"
)

# Inicialización de la base de datos
engine = get_engine()
Base.metadata.create_all(bind=engine)

app.include_router(
    lanzamientos_espaciales_router.router,
    prefix="/lanzamientos_espaciales",
    tags=["Lanzamientos Espaciales"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 