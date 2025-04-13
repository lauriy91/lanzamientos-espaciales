# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import boto3
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

# Configuración de PostgreSQL
USUARIO_POSTGRES = os.getenv("DB_USER", "postgres")
CONTRASENA_POSTGRES = os.getenv("DB_PASSWORD", "")
HOST_POSTGRES = os.getenv("DB_HOST", "localhost")
PUERTO_POSTGRES = os.getenv("DB_PORT", "5432")
NOMBRE_DB_POSTGRES = os.getenv("DB_NAME", "spacex_dev")

URL_BASE_DATOS = f"postgresql+psycopg2://{USUARIO_POSTGRES}:{CONTRASENA_POSTGRES}@{HOST_POSTGRES}:{PUERTO_POSTGRES}/{NOMBRE_DB_POSTGRES}"

# Configuración de SQLAlchemy
motor = create_engine(URL_BASE_DATOS)
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)
Base = declarative_base()

# Configuración de DynamoDB
NOMBRE_TABLA_DYNAMODB = os.getenv("LAUNCHES_TABLE", "lanzamientos")
REGION_AWS = os.getenv("AWS_REGION", "us-east-1")


# Cliente de DynamoDB configurado
def obtener_cliente_dynamodb():
    return boto3.resource("dynamodb", region_name=REGION_AWS)


def obtener_tabla_dynamodb():
    dynamodb = obtener_cliente_dynamodb()
    return dynamodb.Table(NOMBRE_TABLA_DYNAMODB)


# Función para obtener la sesión de base de datos
def obtener_db():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()


def es_desarrollo():
    return os.getenv("ENVIRONMENT", "development").lower() == "development"
