FROM cgr.dev/chainguard/python:latest-dev

# Directorio de trabajo
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Puerto disponble
EXPOSE 8000

# Ejecutar la aplicación
CMD ["uvicorn", "web.main:app", "--host", "0.0.0.0", "--port", "8000"] 