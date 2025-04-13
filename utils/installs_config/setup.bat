@echo off

@REM Crear entorno virtual si no existe
if not exist .venv (
    python -m venv .venv
)

@REM Activar entorno virtual
call .venv\Scripts\activate.bat

@REM Instalar dependencias
pip install -r requirements.txt

REM Instalar AWS CDK globalmente
npm install -g aws-cdk

echo Configuración completada. Entorno virtual activado. 