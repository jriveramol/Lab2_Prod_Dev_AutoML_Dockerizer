from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import log_loss
from sklearn.naive_bayes import GaussianNB
from functools import partial
from sklearn.svm import SVC
from preprocess import *
import numpy as np
import logging
import optuna
import joblib

# Instanciar log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configurar el nivel de logging de Optuna
optuna.logging.set_verbosity(logging.WARNING)

def optimizacion_modelo(trial, nombre_modelo, clase_modelo, params, X_train, y_train, X_test, y_test):
    params_trial = dict()
    for key, value in params.items():
        params_trial[key] = trial.suggest_categorical(key, value)
    
    if nombre_modelo in ['KNN', 'NaiveBayes']:
        model = clase_modelo(**params_trial)
    else:
        model = clase_modelo(**params_trial, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred_proba = model.predict_proba(X_test)
    
    return log_loss(y_test, y_pred_proba)

def train_model(input_file, modelo, target, trials):
    '''Entrenamiento y optimización de modelos'''
    X_train, y_train, X_test, y_test, X_val, y_val = clean_data(input_file, target)
    if modelo == 'NaiveBayes':
        X_train = X_train.toarray()
        X_test = X_test.toarray()
        X_val = X_val.toarray()

    # Modelos a usar
    modelos = {'RandomForest' : RandomForestClassifier,
               'GradientBoosting' : GradientBoostingClassifier,
               'SVM' : SVC,
               'KNN' : KNeighborsClassifier,
               'NaiveBayes' : GaussianNB
               }
    
    # Parámetros de optimización
    parameters = {'RandomForest' : {'n_estimators': [50, 100, 150, 200, 250, 300],
                                    'max_depth': [None, 5, 10, 15, 20, 25],
                                    'min_samples_split': [2, 5, 10],
                                    'min_samples_leaf': [1, 2, 4]},
                  'GradientBoosting' : {'n_estimators': [50, 100, 150, 200, 250],
                                        'learning_rate': [0.01, 0.05, 0.1, 0.2, 0.3],
                                        'max_depth': [3, 5, 7, 10, 15],
                                        'min_samples_split': [2, 5, 10],
                                        'min_samples_leaf': [1, 2, 4],
                                        'subsample': [0.5, 0.7, 0.8, 1.0]},
                  'SVM' : {'C': [0.1, 1, 10, 100, 1000],
                           'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
                           'degree': [2, 3, 4, 5],
                           'gamma': ['scale', 'auto'],
                           'probability': [True]},
                  'KNN' : {'n_neighbors': [3, 5, 7, 10, 15, 20],
                           'weights': ['uniform', 'distance'],
                           'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                           'leaf_size': [10, 20, 30, 40, 50]},
                  'NaiveBayes' : {'var_smoothing': [1e-12, 1e-11, 1e-10, 1e-9, 1e-8]}
                }
    logging.info(f'Entrenando y optimizando modelo {modelo}')
    # Entrenar modelo
    study = optuna.create_study(direction='minimize')
    study.optimize(partial(optimizacion_modelo, 
                           nombre_modelo=modelo,
                           clase_modelo=modelos[modelo], 
                           params=parameters[modelo],
                           X_train=X_train, 
                           y_train=y_train, 
                           X_test=X_test, 
                           y_test=y_test), 
                           n_trials=trials)
    best_params = study.best_params

    if modelo in ['KNN', 'NaiveBayes']:
        best_model = modelos[modelo](**best_params)
    else:
        best_model = modelos[modelo](**best_params, random_state=42)
    best_model.fit(X_train, y_train)

    y_pred_proba = best_model.predict_proba(X_val)
    y_pred = np.argmax(y_pred_proba, axis=1)

    # Precisión
    accuracy = accuracy_score(y_val, y_pred)
    logging.info(f'Precisión: {accuracy:.4f}')

    # F1-Score (macro o weighted)
    f1 = f1_score(y_val, y_pred, average='weighted') 
    logging.info(f'F1-Score: {f1:.4f}')

    # Matriz de confusión
    conf_matrix = confusion_matrix(y_val, y_pred)
    logging.info(f'Matriz de Confusión:\n {conf_matrix}')

    model_name = f'{modelo}.pkl'
    joblib.dump(best_model, model_name)
    
    logging.info(f'Parametros optimizados: {best_params}')
    logging.info(100*'-')