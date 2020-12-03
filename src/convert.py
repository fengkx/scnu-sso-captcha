import os
from os.path import join

from model import load_model
import tensorflowjs as tfjs

__dirname = os.path.dirname(os.path.abspath(__file__))
model = load_model()
tfjs.converters.save_keras_model(model, join(__dirname, '..', 'web-model'))
