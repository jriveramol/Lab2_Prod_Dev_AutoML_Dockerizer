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

# Variable de entorno para elegir deployment_type
ARG DEPLOYMENT_TYPE
ENV DEPLOYMENT_TYPE=$DEPLOYMENT_TYPE

# Como se ejecuta
ENTRYPOINT ["sh", "-c"]
CMD ["if [ \"$DEPLOYMENT_TYPE\" = \"Batch\" ]; then python batch_predict.py; else python api_predict.py; fi"]