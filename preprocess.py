from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import pandas as pd
import logging
import joblib

# Instanciar log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(input_file):
    '''Carga la data'''
    logging.info(f'Cargando archivo {input_file}')
    # try:
    data = pd.read_parquet(input_file)
    logging.info(f'Archivo cargado con exito.')
    # except:
    #     logging.error(f'Error al cargar archivo.')
    logging.info(100*'-')
    return data

def null_data(data):
    '''Muestra la cantidad de valores nulos por columna'''
    missing_summary = data.isnull().sum()
    logging.info("Valores faltantes por columna:")
    logging.info(f'\n{missing_summary}')
    logging.info(100*'-')
    return missing_summary

def data_division(X, y, test_size, random_state):
    '''División de dataset'''
    logging.info("Dividiendo dataset")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, test_size=0.5, random_state=random_state)
    
    logging.info(f'Cant. registros set entrenamiento: {len(X_train)}')
    logging.info(f'Cant. registros set prueba: {len(X_test)}')
    logging.info(f'Cant. registros set validacion: {len(X_val)}')
    logging.info(100*'-')
    return X_train, y_train, X_test, y_test, X_val, y_val

def transform_data(data, target):
    '''Decodificación, escalado e imputación de variables'''
    X = data.drop(columns=[target]).copy()
    y = data[target].copy()

    # Codificación de target
    logging.info(f"Codificando variable {target}")
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    logging.info("Creando preprocesador")
    prop = int(0.75*X.shape[0])
    
    numeric_features = X.select_dtypes(include='number').columns.to_list()
    numeric_features = [feature for feature in numeric_features if len(X[feature].unique()) < prop and 'name' not in feature.lower() and 'id' not in feature.lower()]
    categorical_features = X.select_dtypes(include=['object','category']).columns.to_list()
    categorical_features = [feature for feature in categorical_features if len(X[feature].unique()) < prop and 'name' not in feature.lower() and 'id' not in feature.lower()]
    
    # Pipeline para variables numéricas: imputación de nulos + estandarización
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])
    # Pipeline para variables categóricas: imputación de nulos + one-hot encoding
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    # Unir los transformers
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    # Dividir el dataset en 3 partes: entrenamiento (80%), validación (10%), y prueba (10%)
    X_train, y_train, X_test, y_test, X_val, y_val = data_division(X, y_encoded, 0.2, 42)
    
    # Se aplica el preprocesador
    logging.info("Aplicando preprocesador")
    X_train_processed = preprocessor.fit_transform(X_train)

    # Se exporta el preprocesador
    logging.info("Preprocesador exportado")
    joblib.dump(preprocessor, "preprocessor.pkl")

    X_val_processed = preprocessor.transform(X_val)
    X_test_processed = preprocessor.transform(X_test)
    logging.info(100*'-')
    return X_train_processed, y_train, X_test_processed, y_test, X_val_processed, y_val

def clean_data(input_path, target):
    data = load_data(input_path)
    null_data(data)

    X_train, y_train, X_test, y_test, X_val, y_val = transform_data(data, target)
    return X_train, y_train, X_test, y_test, X_val, y_val