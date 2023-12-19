import pandas as pd
import numpy as np
from PIL import Image
import os
from mfnet.ml_logic.model import initialize_model, compile_model, train_model, evaluate_model
from mfnet.ml_logic.registry import load_model, save_model, save_results, mlflow_run, mlflow_transition_model
import pickle


def preprocess() -> None:
    """
    - Read all images and csv'sfrom /raw_data folder and store it in pickle files
    - Pre process this data and cache it.
    """

    print("\n ⭐️ Use case: preprocess")

    """
    Import csv files
    """

    cwr = os.getcwd()
    index = pd.read_csv(os.path.join(cwr, "raw_data", "index.csv"))
    test = pd.read_csv(os.path.join(cwr, "raw_data", "test.csv"))

    """
    Import train and test images
    """

    images = []
    tests = []
    for path in index['path']:
        image = np.asarray(
            Image.open(os.path.join(cwr, "raw_data", path))
            .resize((224, 224))
        ) / 255
        images.append(image)

    for path in test['path']:
        image = np.asarray(
            Image.open(os.path.join(cwr, "raw_data", path))
            .resize((224, 224))
        ) / 255
        tests.append(image)

    X_train = np.stack(images, axis=0)
    X_test = np.stack(tests, axis=0)

    """
    Get y train and test from dataframes
    """

    y_train = np.array(index['class_id']) - 1
    y_test = np.array(test['class_id']) - 1

    """
    Store variables in pickle files for faster loading
    """

    with open(os.path.join(cwr, "cached_data", "preprocessed", 'X_train.pkl'), 'wb') as file:
        pickle.dump(X_train, file)
    with open(os.path.join(cwr, "cached_data", "preprocessed", 'X_test.pkl'), 'wb') as file:
        pickle.dump(X_test, file)
    with open(os.path.join(cwr, "cached_data", "preprocessed", 'y_train.pkl'), 'wb') as file:
        pickle.dump(y_train, file)
    with open(os.path.join(cwr, "cached_data", "preprocessed", 'y_test.pkl'), 'wb') as file:
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

    cwr = os.getcwd()

    with open(os.path.join(cwr, "cached_data", "preprocessed", 'X_train.pkl'), 'rb') as file:
        X_train = pickle.load(file)

    with open(os.path.join(cwr, "cached_data", "preprocessed", 'X_test.pkl'), 'rb') as file:
        X_test = pickle.load(file)

    with open(os.path.join(cwr, "cached_data", "preprocessed", 'y_train.pkl'), 'rb') as file:
        y_train = pickle.load(file)

    with open(os.path.join(cwr, "cached_data", "preprocessed", 'y_test.pkl'), 'rb') as file:
        y_test = pickle.load(file)

    nb_classes = len(set(y_train))
    print(f"ℹ️ Detected {nb_classes} classes.")
    model = initialize_model(nb_labels=nb_classes)

    model = compile_model(model, learning_rate=learning_rate)

    model, history = train_model(
        model,
        X_train,
        y_train,
        X_test,
        y_test,
        patience=10
    )
    val_accuracy = np.max(history.history['val_accuracy'])
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


@mlflow_run
def evaluate(stage: str = "Production"):
    """
    Evaluate the performance of the latest production model on processed data
    Return val_accuracy as a float
    """
    print("\n⭐️ Use case: evaluate")

    model = load_model(stage=stage)
    assert model is not None
    cwr = os.getcwd()

    with open(os.path.join(cwr, "cached_data", "preprocessed", 'X_test.pkl'), 'rb') as file:
        X_test = pickle.load(file)
    with open(os.path.join(cwr, "cached_data", "preprocessed", 'y_test.pkl'), 'rb') as file:
        y_test = pickle.load(file)

    metrics_dict = evaluate_model(model=model, X=X_test, y=y_test)

    params = dict(
        context="evaluate",
        label_count=len(set(y_test)),
        row_count=len(X_test)
    )

    save_results(params=params, metrics=metrics_dict)

    print("✅ evaluate() done \n")

    return metrics_dict["accuracy"]


def pred(X_pred: np.ndarray = None, y_true: int = None) -> np.ndarray:
    """
    Make a prediction using the latest trained model
    """

    print("\n⭐️ Use case: predict")

    cwd = os.getcwd()
    if X_pred is None:
        with open(os.path.join(cwd, "cached_data", "preprocessed", 'X_test.pkl'), 'rb') as file:
            X_test = pickle.load(file)

        with open(os.path.join(cwd, "cached_data", "preprocessed", 'y_test.pkl'), 'rb') as file:
            y_test = pickle.load(file)

        sample_index = np.random.randint(len(X_test))
        X_pred = np.expand_dims(X_test[sample_index], axis=0)
        y_true = y_test[sample_index] + 1
    else:
        X_pred = np.expand_dims(X_pred, axis=0) / 255.0

    metadata = pd.read_csv(os.path.join(cwd, "raw_data", "metadata.csv"), index_col='class_id')

    model = load_model()
    assert model is not None

    y_preds = model.predict(X_pred)[0]
    y_pred_max = np.max(y_preds)
    y_pred_class = np.argmax(y_preds) + 1
    y_pred_metadata = metadata.loc[y_pred_class]
    y_pred_metadata['prob'] = y_pred_max

    print("\nℹ️  Prediction done:\n", y_preds)
    print(y_pred_metadata)

    if y_true:
        print("\n✅ Correct match" if y_pred_class == y_true else "\n⛔️ Wrong match")

        y_true_metadata = metadata.loc[y_true]
        y_true_metadata['prob'] = y_preds[y_true-1]
        print("y_true:\n", y_true_metadata)

    return y_pred_metadata


if __name__ == '__main__':
    # preprocess()
    # train()
    evaluate()
    # pred()
