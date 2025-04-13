#!/bin/bash

# Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

# Activar entorno virtual
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar AWS CDK globalmente
npm install -g aws-cdk

echo "Configuración completada. Entorno virtual activado." 