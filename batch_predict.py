from train import *
import pandas as pd
import logging
import joblib
import shutil
import os

# Instanciar log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_env():
    # Acceder a las variables
    input_file = os.getenv("DATASET")
    target = os.getenv("TARGET")
    modelo = os.getenv("MODEL")
    trials = int(os.getenv("TRIALS"))
    input_folder = os.getenv("INPUT_FOLDER")    
    output_folder = os.getenv("OUTPUT_FOLDER")

    # Mostrar las variables
    logging.info('PARAMETROS DE EJECUCION:')
    logging.info(f'INPUT_FILE: {input_file}')
    logging.info(f'TARGET: {target}')
    logging.info(f'MODEL: {modelo}')
    logging.info(f'TRIALS: {trials}')
    logging.info(f'INPUT_FOLDER: {input_folder}')
    logging.info(f'OUTPUT_FOLDER: {output_folder}')

    logging.info(100*'-')
    return input_file, target, modelo, trials, input_folder, output_folder

def load_model(modelo):
    # Carga de modelo
    logging.info("Cargando modelo")
    model = joblib.load(f'{modelo}.pkl')
    return model

def load_preprocessor():
    # Carga de preprocesador
    logging.info("Cargando preprocesador")
    preprocessor = joblib.load('preprocessor.pkl')
    return preprocessor
    
def batch_prediction():
    # Lectura de variables
    input_file, target, modelo, trials, input_folder, output_folder = load_env()

    # Entrenamiento
    train_model(input_file, modelo, target, trials)

    logging.info(f'ESPERANDO POR DATA EN {input_folder} PARA REALIZAR PREDICCIONES')
    while True:
        files = os.listdir(input_folder)
        if len(files) > 0:
            for file in files:
                logging.info(f'Procesando {file}')
                path_actual = os.path.join(input_folder,file)
                path_destino = os.path.join(os.getcwd(), 'entradas_procesadas', file)
                # Cargar datos de entrada
                logging.info("Cargando datos de entrada")
                data = pd.read_parquet(input_file)

                # Carga de preprocesador y modelo
                preprocessor = load_preprocessor()
                model = load_model(modelo)

                # Aplicar preprocesador
                X = preprocessor.transform(data)

                # Realizamos predicciones
                logging.info("Realizamos predicciones")
                predictions = model.predict_proba(X)
                nombres_columnas = [f'Clase_{no_class+1}' for no_class in range(predictions.shape[1])]
                (pd.DataFrame(predictions, columns=nombres_columnas)
                 .to_parquet(f'{output_folder}/{modelo}_predictions.parquet'))
                
                logging.info(f'Predicciones exportadas en {output_folder}')
                # Mover archivo para que no se vuelva a pocesar
                shutil.move(path_actual, path_destino)
                logging.info(100*"-")
            break
    
    logging.info('Proceso finalizado')

# if __name__ == '__main__':
#     input_file, target, modelo, trials, input_folder, output_folder = load_env()
#     batch_prediction(input_file, target, modelo, trials, input_folder, output_folder)