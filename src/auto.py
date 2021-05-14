import requests
import os
from model import load_model
from dataset import cv_im_process, vec2text
import model
import cv2
import numpy as np
from os.path import join
import shutil
__dirname = os.path.dirname(os.path.abspath(__file__))

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Host': 'sso.scnu.edu.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://sso.scnu.edu.cn',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'

}
model = load_model()
rand_path = '/tmp/qwsadasger12adasdasdw'
with requests.Session() as client:
    for i in range(200):
        r = client.get(
            'https://sso.scnu.edu.cn/AccountService/user/rancode.jpg', headers=headers, stream=True)
        with open(rand_path, 'w+b') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        x = cv_im_process(cv2.imread(rand_path), flatten=False, normalize=True)

        p = model.predict(np.array([x]))
        code = vec2text(p[0])
        data = {
            'random': code
        }
        print(data)
        rr = client.post('https://sso.scnu.edu.cn/AccountService/user/checkrandom.html',
                         headers=headers,
                         data=data
                         )
        is_correct = rr.json()['msgcode'] == 0
        print(is_correct, i)
        if not is_correct:
            dst = join(__dirname, 'dataset', 'codes', 'incorrect', code)
            shutil.copyfile(rand_path, dst=dst)
        else:
            dst = join(__dirname, 'dataset', 'codes', 'correct', code)
            shutil.copyfile(rand_path, dst=dst)
