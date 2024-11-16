from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
import pandas as pd
from train import *
import logging
import joblib
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='api.env')

# Instanciar log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Acceder a las variables
input_file = os.getenv("DATASET")
target = os.getenv("TARGET")
modelo = os.getenv("MODEL")
trials = int(os.getenv("TRIALS"))
port = int(os.getenv("PORT"))
model_folder = os.getenv("MODEL_FOLDER")

# Mostrar las variables
logging.info('PARAMETROS DE EJECUCION:')
logging.info(f'INPUT_FILE: {input_file}')
logging.info(f'TARGET: {target}')
logging.info(f'MODEL: {modelo}')
logging.info(f'TRIALS: {trials}')
logging.info(f'PORT: {port}')
logging.info(f'MODEL_FOLDER: {model_folder}')

# Entrenamiento
train_model(input_file, modelo, target, trials, model_folder)

# Crear instancia de FastAPI
app = FastAPI(
    title=f'API de predicción utilizando {modelo}',
    description=f'Servicio de API para predecir utilizando ML {modelo}',
    version='1.0.0'
)

# Cargar el preprocesador y modelo
logging.info("Cargando preprocesador")
preprocessor = joblib.load('preprocessor.pkl')
logging.info("Cargando modelo")
model = joblib.load(f'{model_folder}/{modelo}.pkl')

class PredictionInput(BaseModel):
    input : List[Dict]

# Verificación del estado de la API
# Decorador: modifica la función get de fastAPI con la health_check function
@app.get('/health', summary='Health check', description='Verificar el estado de la API.')
# Función de health check
async def health_check():
    logging.info("Health check")
    return {"status":"OK"}

# Predicciones con data proveída
@app.post('/predict', summary='Predictions generator', description='Realiza predicciones basado en las features enviadas.')
async def predict(input_data: PredictionInput):
    logging.info('Predict request received')
    try:
        # Convertir la lista de PredictionInput a un dataframe
        df = pd.DataFrame(input_data.input)

        # Preprocesamiento y predicción
        X = preprocessor.transform(df)
        logging.info("Realizamos predicciones")
        prediction = model.predict_proba(X)
        nombres_columnas = [f'Clase_{no_class+1}' for no_class in range(prediction.shape[1])]
        df_prediction = pd.DataFrame(prediction, columns=nombres_columnas)
        probs = []
        for idx in df_prediction.index:
            probs.append(df_prediction.loc[idx].to_dict())

        logging.info('Proceso finalizado')
        # retornamos las predicciones utilizando JSON
        return {'predictions':probs}
    except Exception as e:
        logging.error(f"Prediction failed due to {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
uvicorn.run(app, host='0.0.0.0', port=port)