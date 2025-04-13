# SpaceX - Lanzamientos espaciales

Este proyecto es una aplicación que muestra información sobre los lanzamientos de SpaceX, utilizando una arquitectura serverless en AWS.


## Especificaciones tecnicas
- Programming Language: Python
- Databases: 
  - DynamoDB (Producción)
  - PostgreSQL (Desarrollo local)
- ORM: SQLAlchemy
- Libraries:
  - boto3 - conexiones a la nube
  - aws_cdk - servicios aws
  - fastapi para desarrollo de API
  - psycopg2-binary para PostgreSQL
- uvicorn levantar servicio FastAPI
- Swagger UI para documentación y pruebas de API
- Modulos necesarios y librerias para la aplicacion (in [requirements.txt](./requirements.txt)).


## Modules
spacex_project/
├── infrastructure/           # Código de infraestructura CDK
│   └── app.py               # Stack principal de CDK
├── lambda/                  # Código de la función Lambda
├── web/                    # Aplicación web FastAPI
│   ├── main.py            # Aplicación principal
│   ├── models/            # Modelos de datos
│   ├── database/          # Configuración de bases de datos
│   └── api/               # Endpoints de la API
├── tests/                  # Tests unitarios y de integración
├── .github/                # Configuración de GitHub Actions
│   └── workflows/
├── .env                    # Variables de entorno
├── requirements.txt        # Dependencias del proyecto
└── Dockerfile             # Configuración para construir la imagen Docker


## Requisitos

- Python 3.9 o superior
- AWS CLI configurado (solo para producción)
- CDK CLI instalado (solo para producción)
- Docker (para desarrollo local)
- PostgreSQL (para desarrollo local)


## Project Initialization
- Clonar el repositorio:
  git clone https://github.com/lauriy91/lanzamientos-espaciales.git
- Crear entorno virtual
  python -m venv venv
  source venv/bin/activate
- Instalar dependencias
  pip install -r requirements.txt
- Configurar base de datos local
  createdb spacex_dev
  psql -U postgres
  CREATE DATABASE spacex_dev;


## Configuración Local

Crear archivo `.env` con las siguientes variables:
```env
# Configuración de la aplicación
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True

# Base de datos local
DB_HOST=localhost
DB_PORT=5432
DB_NAME=spacex_dev
DB_USER=postgres
DB_PASSWORD=postgres_password

# AWS (solo para producción)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=tu_access_key_id
AWS_SECRET_ACCESS_KEY=tu_secret_access_key
LAUNCHES_TABLE=spacex_launches_table
VPC_ID=tu-vpc-id
ECR_REPOSITORY=spacex-lanzamientos
```

## Desarrollo Local

1. Iniciar la aplicación:
uvicorn web.main:app --reload

2. Acceder a la documentación Swagger:
- Abrir en navegador: http://localhost:8000/docs
- Interfaz Swagger UI para probar endpoints
- Documentación OpenAPI disponible


## Endpoints

- GET /launches - Listar todos los lanzamientos
- GET /launches/{id} - Obtener detalles de un lanzamiento
- GET /launches/upcoming - Próximos lanzamientos
- GET /launches/past - Lanzamientos pasados


## Testing

Para ejecutar tests:
pytest
pytest --dynamodb-local


## Construir la imagen Docker
- docker build -t spacex-lanzamientos .


## Despliegue en AWS

El despliegue está automatizado mediante GitHub Actions. Cada push a la rama principal activa:
1. Pruebas automatizadas
2. Despliegue de la función Lambda
3. Construcción y push de la imagen Docker a ECR
4. Actualización del servicio ECS

## Para desplegar manualmente la infraestructura:
```bash
cd infrastructure
cdk deploy
```