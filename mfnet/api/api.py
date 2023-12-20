import numpy as np
import pandas as pd
import os

from fastapi import FastAPI, UploadFile, File
from PIL import Image

from mfnet.interface.workflow import train_flow
from mfnet.ml_logic.registry import load_model


def load_in_cache(api: FastAPI) -> None:
    api.state.model = load_model()
    assert api.state.model is not None

    cwd = os.getcwd()
    api.state.metadata = pd.read_csv(os.path.join(cwd, "raw_data", "metadata.csv"), index_col='class_id')
    assert api.state.metadata is not None


api = FastAPI()
load_in_cache(api)


@api.get("/")
def get_status():
    return {"status": "ok"}


@api.post("/predict")
async def predict(img: UploadFile = File(...)) -> dict:
    # Receiving and decoding the image
    contents = await img.read()
    image_array = np.fromstring(contents, np.uint8)
    X_pred = image_array.reshape(224, 224, 3)

    image = Image.fromarray(X_pred)
    image.save(os.path.join(os.getcwd(), "raw_data", "preds", "predict.png"))

    # Predicting

    y_pred = model_predict(X_pred=X_pred, y_true=None)

    # Sending result back
    res = {
        'probability': float(y_pred.prob),
        'minifigure_name': y_pred.minifigure_name,
        'set_id': str(eval(y_pred.lego_ids)[0]),
        'set_name': eval(y_pred.lego_names)[0],
        'class_id': int(y_pred.name + 1)
    }
    return res


def model_predict(X_pred: np.ndarray, y_true: int = None):
    X_pred = np.expand_dims(X_pred, axis=0) / 255.0

    y_preds = api.state.model.predict(X_pred)[0]
    y_pred_max = np.max(y_preds)
    y_pred_class = np.argmax(y_preds) + 1
    y_pred_metadata = api.state.metadata.loc[y_pred_class]
    y_pred_metadata['prob'] = y_pred_max

    print("\nℹ️  Prediction done:\n", y_preds)
    print(y_pred_metadata)

    if y_true:
        print("\n✅ Correct match" if y_pred_class == y_true else "\n⛔️ Wrong match")

        y_true_metadata = api.state.metadata.loc[y_true]
        y_true_metadata['prob'] = y_preds[y_true-1]
        print("y_true:\n", y_true_metadata)

    return y_pred_metadata


@api.post("/add_img_train")
def add_img_train(class_id: int) -> None:
    """
    Moves image to another folder
    """
    source = os.path.join(os.getcwd(), "raw_data", "preds", "predict.png")
    destination_folder = os.path.join(os.getcwd(), "raw_data", "added_data")
    files_count = len(os.listdir(destination_folder))
    final_file = os.path.join(destination_folder, f"{files_count+1}.png")
    os.rename(source, final_file)
    """
    Adds path and label to the train csv then tries training a new, better model
    """
    df = pd.DataFrame({
        'path': [f'added_data/{files_count+1}.png'],
        'class_id': [class_id]
    })
    csv_path = os.path.join(os.getcwd(), "raw_data", "index.csv")
    df.to_csv(f"{csv_path}", mode='a', header=False, index=False)
    train_flow(force=True)
    load_in_cache(api)


@api.get("/retrain")
def retrain():
    return {"Workflow": train_flow()}


@api.post("/add_class")
async def add_class(imgs: list,
                    lego_ids: str,
                    lego_names: str,
                    minifigure_name: str
                    ) -> None:
    """
    Splits images 3/4 train and 1/4 test
    Saves images in added_data or test folder
    adds path and class_id to test and train csv
    add new class in metadata csv
    Force new model into production
    """
    test = imgs[::4]
    train = [img for img in imgs if img not in test]
    cwd = os.getcwd()
    test_csv_path = os.path.join(os.getcwd(), "raw_data", "test.csv")
    train_csv_path = os.path.join(os.getcwd(), "raw_data", "index.csv")
    metadata_csv_path = os.path.join(cwd, "raw_data", "metadata.csv")
    metadata = pd.read_csv(metadata_csv_path, index_col='class_id')
    label = max(metadata.index)+1

    for img in test:
        contents = await img.read()
        image_array = np.fromstring(contents, np.uint8)
        temp = image_array.reshape(224, 224, 3)
        image = Image.fromarray(temp)
        destination_folder = os.path.join(os.getcwd(), "raw_data", "test")
        files_count = len(os.listdir(destination_folder))
        image.save(os.path.join(destination_folder, f"{files_count+1}.jpg"))
        df = pd.DataFrame({
            'path': [f'test/{files_count+1}.jpg'],
            'class_id': [label]
        })
        df.to_csv(f"{test_csv_path}", mode='a', header=False, index=False)

    for img in train:
        contents = await img.read()
        image_array = np.fromstring(contents, np.uint8)
        temp = image_array.reshape(224, 224, 3)
        image = Image.fromarray(temp)
        destination_folder = os.path.join(os.getcwd(), "raw_data", "added_data")
        files_count = len(os.listdir(destination_folder))
        image.save(os.path.join(destination_folder, f"{files_count+1}.jpg"))
        df = pd.DataFrame({
            'path': [f'added_data/{files_count+1}.jpg'],
            'class_id': [label]
        })
        df.to_csv(f"{train_csv_path}", mode='a', header=False, index=False)

    df = pd.DataFrame({
        'class_id': [label],
        'lego_ids': [f'[{lego_ids}]'],
        'lego_names': [f'["{lego_names}"]'],
        'minifigure_name': [minifigure_name]
    })
    df.to_csv(f"{metadata_csv_path}", mode='a', header=False, index=False)
    train_flow(force=True)
    load_in_cache(api)


@api.get("/retrieve_metadata")
def retrieve_metadata() -> dict:
    metadata_csv_path = os.path.join(os.getcwd(), "raw_data", "metadata.csv")
    metadata = pd.read_csv(metadata_csv_path, index_col='class_id')

    response = {
        f"{row['lego_ids']} {row['lego_names']} {row['minifigure_name']}":
        index for index, row in metadata.iterrows()
    }
    return response
