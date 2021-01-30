#! python
# https://github.com/GantMan/nsfw_model

import argparse
import json
import os
from os import listdir
from os.path import isfile, join, exists, isdir, abspath

import numpy as np
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub

from . import utils
from auto_everything.disk import Disk

disk = Disk()

IMAGE_DIM = 224  # required/default image dimensionality


def load_images_from_arrays(image_paths, image_size, verbose=True):
    loaded_images = []
    loaded_image_paths = []


def load_model(model_path):
    if model_path is None or not exists(model_path):
        raise ValueError("saved_model_path must be the valid directory of a saved model to load.")

    model = tf.keras.models.load_model(model_path, custom_objects={'KerasLayer': hub.KerasLayer})
    return model


def classify_nd(model, nd_images):
    """ Classify given a model, image array (numpy)...."""

    model_preds = model.predict(nd_images)
    # preds = np.argsort(model_preds, axis = 1).tolist()

    categories = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']

    probs = []
    for i, single_preds in enumerate(model_preds):
        single_probs = {}
        for j, pred in enumerate(single_preds):
            single_probs[categories[j]] = float(pred)
        probs.append(single_probs)
    return probs


class NSFWDetector():
    def __init__(self):
        MODEL_FILE_NAME = "nsfw_detection_model.h5"
        MODEL_PATH = os.path.join(utils.ROOT_DIR, MODEL_FILE_NAME)

        if not utils.disk.exists(MODEL_PATH):
            print("downloading...")
            utils.network.download("https://github.com/yingshaoxo/pornstar/raw/master/models/" + MODEL_FILE_NAME,
                                   MODEL_PATH)
            print(f"{MODEL_FILE_NAME} was downloaded!")

        self.model = load_model(MODEL_PATH)

    def detect(self, numpyImage):
        tempFile = disk.getATempFilePath("temp.jpg")
        utils.save_a_frame_as_an_image(tempFile, numpyImage)
        image = keras.preprocessing.image.load_img(tempFile, target_size=(IMAGE_DIM, IMAGE_DIM))
        image = keras.preprocessing.image.img_to_array(image)
        image /= 255
        probs = classify_nd(self.model, np.asarray([image]))
        os.remove(tempFile)
        return probs
        """
        numpyImage = keras.preprocessing.image.smart_resize(numpyImage, size=(IMAGE_DIM, IMAGE_DIM),
                                                            interpolation="nearest")
        numpyImage = numpyImage.astype(np.float)
        numpyImage /= 255
        probs = classify_nd(self.model, np.asarray([numpyImage]))
        """

    def isPorn(self, numpyImage, threshold=0.9):
        result = self.detect(numpyImage)[0]
        if result["porn"] > threshold:
            return True
        else:
            return False


if __name__ == "__main__":
    pass
