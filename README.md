# SpaceX - Lanzamientos espaciales

Este proyecto es una aplicación que muestra información sobre los lanzamientos de SpaceX, utilizando una arquitectura serverless en AWS.


## Especificaciones tecnicas
- Programming Language: Python
- Database: Dynamo
- ORM: sqlAlchemy
- Libraries:
  - boto3 - conexiones a la nube
  - aws_cdk - servicios aws
  - fastapi para desarrollo de API
- uvicorn levantar servicio FastAPI
- Modulos necesarios y librerias para la aplicacion (in [requirements.txt](./requirements.txt)).


## Modules
spacex_project/
├── infrastructure/           # Código de infraestructura CDK
│   └── app.py               # Stack principal de CDK
├── lambda/                  # Código de la función Lambda
├── web/                    # Aplicación web FastAPI
├── tests/                  # Tests unitarios y de integración
├── .github/                # Configuración de GitHub Actions
│   └── workflows/
├── .env                    # Variables de entorno
├── requirements.txt        # Dependencias del proyecto
└── Dockerfile             # Configuración para construir la imagen Docker


## Requisitos

- Python 3.9 o superior
- AWS CLI configurado
- CDK CLI instalado
- Docker (para desarrollo local)


## Project Initialization
- Clonar el repositorio:
  git clone https://github.com/lauriy91/lanzamientos-espaciales.git
- Crear entorno virtual
  python -m venv venv
  source venv/bin/activate
- Instalar dependencias
  pip install -r requirements.txt


## Endpoints

- GET /sales/product
- GET /sales/day
- GET /sales/category
- GET /sales/outliers


## Como levantar el proyecto:
- cd lanzamiento_espaciales
- venv\Scripts\activate
- uvicorn web.main:app --reload


## Construir la imagen Docker
- docker build -t spacex-lanzamientos .


## Ejecutar test
- pytest


## Despliegue

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