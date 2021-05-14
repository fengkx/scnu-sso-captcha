import os
from os.path import join
from dataset import cv_im_process,  load_dataset, text2vec, vec2text
from model import get_model, checkpoint_predict, load_model
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, Callback as TfCallback
from config import OUTPUT_DIR
class EpochPredictCallback(TfCallback):
    def on_epoch_end(self, epoch, logs=False):
        model = self.model
        checkpoint_predict(model, x_test, t_test)


(x_train, t_train), (x_test, t_test) = load_dataset()


print('shapes: ', x_train.shape, t_test.shape)
model = load_model()
history = model.fit(
    x_train,
    t_train,
    batch_size=300,
    epochs=10,
    validation_split=0.2,
    callbacks=[EpochPredictCallback()]
    )
test_scores = model.evaluate(x_test, t_test, verbose=2)
print("Test loss:", test_scores[0])
print("Test accuracy:", test_scores[1])
model.save(OUTPUT_DIR)

new_model = tf.keras.models.load_model(OUTPUT_DIR)
checkpoint_predict(new_model, x_test, t_test)

# xx = cv_im_process(cv2.imread('./U6cG.jpg'), flatten=False, normalize=True)
# p = new_model.predict(np.array([xx]))
# print(vec2text(p[0]))
