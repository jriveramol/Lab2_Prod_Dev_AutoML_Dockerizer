# Lab2_Prod_Dev_AutoML_Dockerizer
Repositorio dedicado a la creación de pipeline de autoML con Docker con dos métodos de despliegue:
1. Batch
2. API

## Construcción de Imagen
```
# Moverse a ruta donde se descargó el Dockerfile
cd "/mnt/c/path"

# Construir la imagen con el siguiente comando (el nombre automl-dockerizer y el tag latest puede cambiar)
docker build -t automl-dockerizer:latest .
```
