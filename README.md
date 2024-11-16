# Lab2_Prod_Dev_AutoML_Dockerizer
Repositorio dedicado a la creación de pipeline optimizado de autoML con Docker con dos métodos de despliegue:
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
- **oP:** trabaja en conjunto con *grep*, y su función es extraer solamente el valor después del *"="*. En este ejemplo, el resultado es *8000*.

## Archivos
##### batch.env
Contiene los parámetros de ejecución en modo **batch**.
```
 DATASET=data/data.parquet                   # Path al dataset con el que se entrenará, optimizará y evaluará el modelo
 TARGET=Survived                             # Característica del dataset que se busca predecir
 MODEL=SVM                                   # Tipo de modelo a entrenar, puede ser RandomForest, GradientBoosting, SVM, KNN o NaiveBayes
 TRIALS=10                                   # Cantidad de trials que Optuna ejecutará para optimizar los parámetros del modelo seleccionado
 DEPLOYMENT_TYPE=Batch                       # Modo de despliegue
 INPUT_FOLDER=/data/input                    # Carpeta en la que se estará a la espera de datos para realizar predicciones con el modelo entrenado y optimizado
 OUTPUT_FOLDER=/data/output                  # Carpeta en la que se exportarán las predicciones realizadas por el modelo
 PROCESSED_ENTRY=/data/entradas_procesadas   # Carpeta a la que se moverán los datos de entrada colocados en INPUT_FOLDER, con el fin de no reprocesarlos
 MODEL_FOLDER=/data/modelos_entrenados       # Carpeta a la que se exportan los modelos entrenados
```

##### api.env
Contiene los parámetros de ejecución en modo **API**.
```
 DATASET=data/data.parquet                   # Path al dataset con el que se entrenará, optimizará y evaluará el modelo
 TARGET=Survived                             # Característica del dataset que se busca predecir
 MODEL=SVM                                   # Tipo de modelo a entrenar, puede ser RandomForest, GradientBoosting, SVM, KNN o NaiveBayes
 TRIALS=10                                   # Cantidad de trials que Optuna ejecutará para optimizar los parámetros del modelo seleccionado
 DEPLOYMENT_TYPE=Batch                       # Modo de despliegue
 PORT=8000                                   # Puerto en el que se hará el despliegue de la API tanto local como en el contenedor de Docker
 MODEL_FOLDER=/data/modelos_entrenados       # Carpeta a la que se exportan los modelos entrenados
```

##### test_api.ipynb
Archivo que permite realizar pruebas de solicitudes a la API.

##### data_test.parquet
Archivo con muestras de dataset para enviar a la API o para colocar en la carpeta *INPUT_FOLDER* para obtener predicciones.
Para enviarlas a la API ejecute las celdas del cuaderno *test_api.ipynb*.
