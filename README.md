Sistema de seguimiento de lanzamientos espaciales de SpaceX que utiliza AWS para procesamiento y almacenamiento de datos.

## Arquitectura

El sistema está compuesto por los siguientes componentes:

- **API Lambda**: Función Python que obtiene datos de la API pública de SpaceX
- **DynamoDB**: Base de datos para almacenar información de lanzamientos
- **Aplicación Web**: Frontend desplegado en ECS Fargate
- **Pipeline CI/CD**: Automatización con GitHub Actions

## Requisitos Previos

- Python 3.9+
- AWS CLI configurado
- Docker
- Cuenta de GitHub
- Acceso a servicios AWS (DynamoDB, Lambda, ECS, ECR)

## Estructura del Proyecto

lanzamientos_espaciales_project/
├── lambda/                 
├── web/                   
├── infrastructure/        
├── tests/                
└── .github/              


## Configuración Local

1. Clonar el repositorio
2. Instalar dependencias:
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt

3. Configurar variables de entorno:
   cp .env.example .env


## Desarrollo

- Ejecutar pruebas: `pytest`
- Ejecutar aplicación local: `uvicorn web.main:app --reload`
- Construir imagen Docker: `docker build -t lanzamientos-espaciales .`

## Despliegue

El despliegue está automatizado mediante GitHub Actions. Cada push a la rama principal activa:
1. Pruebas automatizadas
2. Construcción de imagen Docker
3. Despliegue en ECS Fargate
4. Actualización de Lambda

## Documentación API - Swagger

La documentación de la API está disponible en `/docs` cuando la aplicación está en ejecución.
