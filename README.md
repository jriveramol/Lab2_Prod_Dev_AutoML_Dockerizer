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
## Modo Batch
En la misma ruta donde se creó la imagen, ejecutar el siguiente comando para crear el contenedor basado en la imagen (si cambió el nombre de autom-dockerizer y el tag, debe sustituirlos en el comando).
```
docker run --rm --name batch_cont --env-file batch.env -v "/mnt/c/path/data":/data automl-dockerizer:latest
```
**Parámetros**
- **rm:** permite eliminar el contenedor automáticamente cuando se detenga.
- **name:** nombre del contenedor, en este ejemplo es *batch_cont*.
- **env-file:** permite indicar qué archivo .env debe leerse, en este ejemplo es *batch.env*.
- **v:** permite indicar el volumen al que se dará acceso a Docker y el nombre del volumen que se creará en el contenedor, en este caso se da acceso a */mnt/c/path/data* y se crea el volumen */data*.
