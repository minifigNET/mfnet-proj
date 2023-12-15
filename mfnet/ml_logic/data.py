import pandas as pd
import numpy as np
from PIL import Image
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def get_data(img_resolution=(224,224)):

    """Importation des csv"""

    cwr = os.getcwd().strip('/notebooks')
    index = pd.read_csv(f'/{cwr}/raw_data/index.csv')
    metadata = pd.read_csv(f'/{cwr}/raw_data/metadata.csv',index_col='class_id')
    test = pd.read_csv(f'/{cwr}/raw_data/test.csv')

    """Importation des images train et test"""

    images = []
    tests = []
    for path in index['path']:
        image = np.asarray(Image.open(f'/{cwr}/raw_data/{path}')\
            .resize(img_resolution)
            )
        images.append(image)
    for path in test['path']:
        image = np.asarray(Image.open(f'/{cwr}/raw_data/{path}')\
            .resize(img_resolution)
            )
        tests.append(image)

    X_train = np.stack(images,axis=0)
    X_test = np.stack(tests,axis=0)

    """Get y train and test from dataframes"""

    y_train = np.array(index['class_id'])
    y_test = np.array(test['class_id'])

    print("✅ data imported")

    return X_train,y_train,X_test,y_test

def data_preprocessing(X_train,y_train,X_test,y_test):

    """Returns standardized data"""
    print("✅ data preprocessed")

    return X_train/255,y_train-1,X_test/255,y_test-1
