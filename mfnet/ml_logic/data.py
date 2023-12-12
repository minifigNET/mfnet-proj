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

    """Get y train and test from dataframes and make values starts from 0"""

    y_train = np.array(index['class_id'])-1
    y_test = np.array(test['class_id'])-1

    print("✅ data imported")

    return X_train,y_train,X_test,y_test

def data_augmentation(X_train,y_train,X_test,y_test):

    """Making the imagedatagenerator for train set"""

    train_datagen = ImageDataGenerator(
    rescale = 1./255,
    featurewise_center = False,
    featurewise_std_normalization = False,
    rotation_range = 10,
    width_shift_range = 0.1,
    height_shift_range = 0.1,
    horizontal_flip = True,
    zoom_range = (0.8, 1.2),
    )

    """Making the imagedatagenerator for test set"""

    test_datagen = ImageDataGenerator(
        rescale = 1./255
    )

    """Making the actual variables that are going to be trained and validated"""

    train_flow = train_datagen.flow(X_train, y_train, batch_size = 16)

    valid_flow = test_datagen.flow(X_test, y_test, batch_size = 1)

    print("✅ data augmented")

    return train_flow,valid_flow
