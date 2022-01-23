import os
import shutil
import urllib.request

from tensorflow.keras.models import load_model as _keras_load_model

from .utils import ROOT_DIR, STATIC_DIR


def useWhiteningModel():
    MODEL_FILE_NAME = "pornstar_whitening_model.h5"
    MODEL_PATH = os.path.join(ROOT_DIR, MODEL_FILE_NAME)

    # Download it from Releases if needed
    if not os.path.exists(MODEL_PATH):
        print(f"Start to download {MODEL_FILE_NAME}...")
        with urllib.request.urlopen(
                "https://github.com/yingshaoxo/pornstar/raw/master/models/" + MODEL_FILE_NAME) as resp, open(MODEL_PATH,
                                                                                                             'wb') as out:
            shutil.copyfileobj(resp, out)
        print(f"{MODEL_FILE_NAME} was downloaded!")

    model = _keras_load_model(MODEL_PATH)

    return model
