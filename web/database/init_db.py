from .config import Base, engine

def inicializar_base_datos():
    """Inicializa la base de datos creando todas las tablas"""
    Base.metadata.create_all(bind=engine)

def eliminar_base_datos():
    """Elimina todas las tablas de la base de datos"""
    Base.metadata.drop_all(bind=engine)

if __name__ == "__main__":
    print("Creando tablas de la base de datos...")
    inicializar_base_datos()
    print("¡Tablas creadas exitosamente!") 