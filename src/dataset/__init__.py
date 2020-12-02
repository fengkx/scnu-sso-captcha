import numpy as np
import cv2
import os
from os import listdir
from os.path import isfile, join
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping, Callback as TfCallback
from config import CASESENTIVE, DICT_LEN, idict
__dirname = os.path.dirname(os.path.abspath(__file__))
marked_path = join(__dirname, 'codes', 'mark')
files = [f for f in listdir(marked_path) if isfile(join(marked_path, f))]
np.random.shuffle(files)

def cv_im_process(img, flatten=False, normalize=False):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    im2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 15)
    im3 = cv2.medianBlur(im2, 3)
    # im3 = im2
    # for i in range(1, im3.shape[0]-1):
    #     for j in range(1, im3.shape[1]-1):
    #         cnt = 0
    #         cnt += np.sum(im3[i-1][j-1:j+2] / 255)
    #         cnt += np.sum(im3[i][j-1:j+2] / 255)
    #         cnt += np.sum(im3[i+1][j-1:j+2] /255)
    #         if cnt <= 3:
    #             im3[i][j] = 0

    im3 = im3
    if flatten:
        im3 = im3.flatten()
    if normalize:
        im3 = im3 / 255
    return im3


def text2vec(code):
    t = np.zeros((len(code), DICT_LEN), np.float)
    for i in range(t.shape[0]):
        t[i][idict.index(code[i])] = 1
    return t

def vec2text(t):
    idx = np.argmax(t, axis=1)
    b = ""
    for i in idx:
        b += idict[i]
    return b

def load_dataset():
    x_all = []
    t_all = []
    for code in files:
        file_path = join(marked_path, code)
        code = code.split('.')[0]
        if not CASESENTIVE:
            code = code.upper()
        img = cv_im_process(cv2.imread(file_path), flatten=False, normalize=True)
        t = text2vec(code)
        x_all.append(img)
        t_all.append(t)
    x_all = np.array(x_all)
    t_all = np.array(t_all)
    # print(x_all.shape, t_all.shape)
    # print('x element shape', x_all[0].shape)
    # print('label element shape',t_all[0].shape)

    total_size = x_all.shape[0]
    test_size = min(int(total_size / 10), 256)
    train_size = int(total_size - test_size)
    # print(total_size, test_size)
    x_train = x_all[:train_size]
    t_train = t_all[:train_size]
    x_test = x_all[train_size:]
    t_test = t_all[train_size:]
    # print('training set', x_train.shape, t_train.shape)
    return (x_train, t_train), (x_test, t_test)