from batch_predict import *
import logging

# Instanciar log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def deployment():
    # Leer tipo de deployment
    deployment_type = os.getenv("DEPLOYMENT_TYPE")
    logging.info(f'Ejecutando deployment {deployment_type}')
    if deployment_type == 'Batch':
        batch_prediction()
    else:
        logging.info('API')

if __name__ == '__main__':
    deployment()