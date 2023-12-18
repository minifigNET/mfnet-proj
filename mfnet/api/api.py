import numpy as np
import pandas as pd
import os
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import pandas as pd
from mfnet.interface.main import pred
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
def index():
    return {"status": "ok"}


@api.post("/predict")
async def predict(img: UploadFile = File(...)) -> dict:
    # Receiving and decoding the image
    contents = await img.read()
    image_array = np.fromstring(contents, np.uint8)
    print(image_array.shape)
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

@api.get("/add_img_train")
def add_img_train(label:int):
    """
    Moves image to another folder
    """
    source = os.path.join(os.getcwd(), "raw_data", "preds", "predict.png")
    destination_folder = os.path.join(os.getcwd(), "raw_data", "added_data")
    files_count = len(os.listdir(destination_folder))
    final_file = os.path.join(destination_folder,f"{files_count+1}.png")
    os.rename(source, final_file)
    """
    Adds path and label to the train csv then tries training a new, better model
    """
    df = pd.DataFrame({
        'path':[f'added_data/{files_count+1}.png'],
        'class_id':[label]
    })
    csv_path = os.path.join(os.getcwd(), "raw_data", "index.csv")
    df.to_csv(f"{csv_path}",mode='a', header=False, index=False)
    return {"Workflow": train_flow()}

@api.get("/retrain")
def retrain():
    return {"Workflow": train_flow()}

# @api.get("/add_class")
# def add_class(label:int,metadata:str):
#     """
#     Splits images 70% train and 30% test
#     """
