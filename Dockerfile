#Base
FROM python:3.12-slim

# Determinamos nuestro directorio de trabajo
WORKDIR /app

# Dependencias y librerías
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && apt-get clean

# Agregamos nuestros archivos
COPY . /app

# Instalar requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Como se ejecuta
ENTRYPOINT ["python", "main.py"]