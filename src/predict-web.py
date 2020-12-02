import os
from os.path import join

from fastapi import FastAPI
from typing import Optional

import cv2
import numpy as np
from model import load_model
from dataset import cv_im_process, vec2text

app = FastAPI()
model = load_model()
__dirname = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/p/{id}")
def read_item(id: int, q: Optional[str] = None):
    file_path = join(__dirname, 'dataset', 'codes', 'raw', f"{id}.jpg")
    x = cv_im_process(cv2.imread(file_path), flatten=False, normalize=True)
    p = model.predict(np.array([x]))
    return vec2text(p[0])
    # return file_path