import sys
import cv2
import numpy as np
from model import load_model
from dataset import cv_im_process, vec2text

model = load_model()
args = sys.argv[1:]

file_path = args[0]
x = cv_im_process(cv2.imread(file_path), flatten=False, normalize=True)
p = model.predict(np.array([x]))
print(vec2text(p[0]))