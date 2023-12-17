from fastapi import FastAPI, UploadFile, File
import numpy as np
import os
from PIL import Image

from mfnet.interface.main import pred

api = FastAPI()


@api.get("/")
def index():
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
    y_pred = pred(X_pred=X_pred, y_true=None)

    # Sending result back
    res = {
        'probability': float(y_pred.prob),
        'minifigure_name': y_pred.minifigure_name,
        'set_id': str(eval(y_pred.lego_ids)[0]),
        'set_name': eval(y_pred.lego_names)[0],
        'class_id': int(y_pred.name + 1)
    }
    return res
