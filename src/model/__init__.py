import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from config import CODE_LEN, DICT_LEN, OUTPUT_DIR
from dataset import text2vec, vec2text

def get_model():
    inputs = keras.Input(shape=(50, 100, 1))
    x = layers.Conv2D(16, 3)(inputs)
    x = layers.Conv2D(16, 3, padding="same")(x)
    x = layers.PReLU()(x)
    x = layers.Conv2D(32, 3)(x)
    x = layers.Conv2D(32, 3, padding="same")(x)
    x = layers.PReLU()(x)
    x = layers.MaxPooling2D(3)(x)
    x = layers.Dropout(0.25)(x)

    x = layers.Conv2D(64, 3)(x)
    x = layers.Conv2D(64, 3, padding="same")(x)
    x = layers.ReLU()(x)
    x = layers.Conv2D(128, 3)(x)
    x = layers.Conv2D(128, 3, padding="same")(x)
    x = layers.ReLU()(x)
    x = layers.MaxPooling2D(3)(x)

    x = layers.Flatten()(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(CODE_LEN * DICT_LEN)(x)
    x = layers.Reshape([CODE_LEN, DICT_LEN])(x)
    outputs = layers.Softmax()(x)
    model = keras.Model(inputs=inputs, outputs=outputs, name="captcha_model")
    model.compile(
        loss="categorical_crossentropy",
        optimizer="Adam",
        metrics=["accuracy"],
    )
    return model

def checkpoint_predict(model, x_test, t_test, batch_size=10):
    random_mask = np.random.choice(x_test.shape[0] ,batch_size)
    x = x_test[random_mask]
    t = t_test[random_mask]
    p = model.predict(x)
    tags = np.array(list(map(vec2text, t)))
    print()
    print('expected: ', tags)
    print('actual: ', np.array(list(map(vec2text, p))))
    pp = model.predict(x_test)
    pc = np.array(list(map(vec2text, pp)))
    ec = np.array(list(map(vec2text, t_test)))
    print('total: ', len(pc), 'correct', np.sum(np.array(pc == ec, np.int)))

def load_model():
    return tf.keras.models.load_model(OUTPUT_DIR)