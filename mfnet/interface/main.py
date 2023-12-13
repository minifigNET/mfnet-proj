import pandas as pd
import numpy as np
from PIL import Image
import os
from mfnet.ml_logic.model import initialize_model,compile_model,train_model,evaluate_model,predict
from mfnet.ml_logic.data import get_data,data_preprocessing
from mfnet.ml_logic.registry import load_model,save_model, save_results,mlflow_run, mlflow_transition_model


import pickle

def preprocess() -> None:
    """
    - Read all images and csv'sfrom /raw_data folder
    - Pre process this data and cache it.
    """

    print("\n ⭐️ Use case: preprocess")

    """Importation des csv"""

    cwr = os.getcwd()
    index = pd.read_csv(f'/{cwr}/raw_data/index.csv')
    metadata = pd.read_csv(f'/{cwr}/raw_data/metadata.csv',index_col='class_id')
    test = pd.read_csv(f'/{cwr}/raw_data/test.csv')

    """Importation des images train et test"""
    images = []
    tests = []
    for path in index['path']:
        image = np.asarray(Image.open(f'/{cwr}/raw_data/{path}')\
            .resize((224,224))
            )
        images.append(image)
    for path in test['path']:
        image = np.asarray(Image.open(f'/{cwr}/raw_data/{path}')\
            .resize((224,224))
            )
        tests.append(image)
    X_train = np.stack(images,axis=0)/255
    X_test = np.stack(tests,axis=0)/255

    """Get y train and test from dataframes"""

    y_train = np.array(index['class_id'])-1
    y_test = np.array(test['class_id'])-1

    """
    Store variables in pickle files for faster loading
    """

    with open('X_train.pkl', 'wb') as file:
        pickle.dump(X_train, file)
    with open('X_test.pkl', 'wb') as file:
        pickle.dump(X_test, file)
    with open('y_train.pkl', 'wb') as file:
        pickle.dump(y_train, file)
    with open('y_test.pkl', 'wb') as file:
        pickle.dump(y_test, file)
