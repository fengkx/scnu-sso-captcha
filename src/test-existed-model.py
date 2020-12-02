import cv2
import numpy as np
from model import load_model
from dataset import cv_im_process, vec2text, load_dataset

model = load_model()
model.summary()



loss_arr = []
acc_arr = []
for i in range(5):
    (x_train, t_train), (x_test, t_test) = load_dataset()
    loss, acc = model.evaluate(x_test,  t_test, verbose=0)
    loss_arr.append(loss)
    acc_arr.append(acc)
print(f"loss: {np.mean(loss_arr)}, accuracy: {np.mean(acc_arr)}")