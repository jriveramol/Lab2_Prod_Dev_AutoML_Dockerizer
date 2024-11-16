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
docker run --rm --name batch_cont --env-file batch.env -v "/mnt/c/your_path/data":/data automl-dockerizer:latest
```
**Parámetros**
- **rm:** permite eliminar el contenedor automáticamente cuando se detenga.
- **name:** nombre del contenedor, en este ejemplo es *batch_cont*.
- **env-file:** permite indicar qué archivo .env debe leerse, en este ejemplo es *batch.env*.
- **v:** permite indicar el volumen al que se dará acceso a Docker y el nombre del volumen que se creará en el contenedor, en este ejemplo se da acceso a */mnt/c/your_path/data* y se crea el volumen */data*.

## Modo API
En la misma ruta donde se creó la imagen, ejecutar el siguiente comando para crear el contenedor basado en la imagen (si cambió el nombre de autom-dockerizer y el tag, debe sustituirlos en el comando).
```
docker run --rm --name api_cont --env-file api.env -v "/mnt/your_path/data":/data -p $(grep -oP 'PORT=\K[0-9]+' api.env):$(grep -oP 'PORT=\K[0-9]+' api.env) automl-dockerizer:latest
```
**Parámetros**
- **rm:** permite eliminar el contenedor automáticamente cuando se detenga.
- **name:** nombre del contenedor, en este ejemplo es *api_cont*.
- **env-file:** permite indicar qué archivo .env debe leerse, en este ejemplo es *api.env*.
- **v:** permite indicar el volumen al que se dará acceso a Docker y el nombre del volumen que se creará en el contenedor, en este ejemplo se da acceso a */mnt/c/your_path/data* y se crea el volumen */data*.
- **p:** permite indicar el puerto que se usará local y el que se creará en Docker, en este ejemplo se indican, para ambos casos, el puerto especificado dentro del archivo *api.env*.
- **grep:** permite hacer una búsqueda de texto con expresiones regulares dentro del archivo indicado, en este caso se busca el texto *PORT=* y cualquier secuencia de números. Como resultado se obtiene algo como *PORT=8000*, en el caso en que el puerto dentro del archivo *api.env* sea 8000.
- **oP:** trabaja en conjunto con *grep*, y su función es extraer solamente el valor después del *=*. En este ejemplo, el resultado es *8000*.
