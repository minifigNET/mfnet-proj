from fastapi import FastAPI, UploadFile, File
import numpy as np

from mfnet.interface.main import pred

api = FastAPI()


@api.get("/")
def index():
    return {"status": "ok"}


@api.post("/predict")
async def batch_predict(img: UploadFile = File(...)) -> dict:
    # Receiving and decoding the image
    contents = await img.read()
    image_array = np.fromstring(contents, np.uint8)
    print(image_array.shape)
    # print(pred(image_array))
    return {"class_name": "Santa 🎅"}
