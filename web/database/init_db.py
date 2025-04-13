from .config import Base, motor

def inicializar_base_datos():
    Base.metadata.create_all(bind=motor)

def eliminar_base_datos():
    Base.metadata.drop_all(bind=motor)

if __name__ == "__main__":
    inicializar_base_datos()