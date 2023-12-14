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
    - Read all images and csv'sfrom /raw_data folder and store it in pickle files
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
    X_train = np.stack(images,axis=0)
    X_test = np.stack(tests,axis=0)

    """Get y train and test from dataframes"""

    y_train = np.array(index['class_id'])
    y_test = np.array(test['class_id'])

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

    print("✅ Data saved locally in pickles")

@mlflow_run
def train(learning_rate=0.0001):
    """
    Load pickle data
    Train model on this data
    Store training results and model weights
    """
    print("\n⭐️ Use case: train")
    print("\nLoading preprocessed validation data...")

    with open('X_train.pkl', 'rb') as file:
        X_train = pickle.load(file) /255

    with open('X_test.pkl', 'rb') as file:
        X_test = pickle.load(file) /255

    with open('y_train.pkl', 'rb') as file:
        y_train = pickle.load(file) -1

    with open('y_test.pkl', 'rb') as file:
        y_test = pickle.load(file) -1

    model = load_model()

    if model is None:
        model = initialize_model(nb_labels=np.max(y_train)+1)

    model = compile_model(model, learning_rate=learning_rate)

    model, history = train_model(
            model,
            X_train,
            y_train,
            X_test,
            y_test,
            patience=10
        )
    val_accuracy = np.max(history.history['accuracy'])
    params = dict(
        context="train",
        label_count=len(y_train),
        image_count=len(X_train),
    )
    save_results(params=params, metrics=dict(accuracy=val_accuracy))

    save_model(model=model)

    mlflow_transition_model(current_stage="None", new_stage="Staging")

    print("✅ train() done \n")

    return val_accuracy

# @mlflow_run
def evaluate(stage: str = "Production"):
    """
    Evaluate the performance of the latest production model on processed data
    Return val_accuracy as a float
    """
    print("\n⭐️ Use case: evaluate")

    model = load_model(stage=stage)
    assert model is not None

    with open('X_test.pkl', 'rb') as file:
        X_test = pickle.load(file)
    with open('y_test.pkl', 'rb') as file:
        y_test = pickle.load(file)

    metrics_dict = evaluate_model(model=model, X=X_test, y=y_test)
    val_accuracy = np.max(metrics_dict.history['accuracy'])

    params = dict(
        context="evaluate",
        label_count=len(y_test),
        row_count=len(X_test)
    )

    save_results(params=params, metrics=metrics_dict)

    print("✅ evaluate() done \n")

def pred(X_pred: pd.DataFrame = None) -> np.ndarray:
    """
    Make a prediction using the latest trained model
    """

    print("\n⭐️ Use case: predict")

    if len(X_pred) == 1:
        image = np.expand_dims(np.asarray(Image.open(X_pred[0]).resize((224, 224))),axis=0)/255
        pred = model.predict(image)
        classe = np.argmax(pred)
        return [(classe+1, pred[0,classe])] # Adding 1 because of the OHE of y_train
    temp=[]
    for image in X_pred:
        temp.append(np.asarray(Image.open(image).resize((224, 224))))
    images_np = np.stack(temp,axis=0) / 255

    model = load_model()
    assert model is not None

    pred = model.predict(images_np)
    print("\n✅ prediction done: ", pred, pred.shape, "\n")

    return pred





if __name__ == '__main__':
    preprocess()
    train()
    # evaluate()
    # pred()
