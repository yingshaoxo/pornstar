import os
import cv2
import numpy as np
import math

from ._PIL_filters import oil_painting

from . import  utils
from .store import *
whitening_model = None
my_dlib = useMyDlib()


def effect_of_blur(frame, kernel=None, method=1):
    if method == 1:
        if (kernel == None):
            kernel = 25
        return cv2.blur(frame, (kernel, kernel))
    elif method == 2:
        if (kernel == None):
            kernel = 25
        return cv2.GaussianBlur(frame, (kernel, kernel), 0)
    elif method == 3:
        if (kernel == None):
            kernel = 39
        else:
            assert (kernel % 2 != 0), "The kernel must be odd!"
        return cv2.medianBlur(frame, kernel)


def effect_of_blur_for_skin(frame, kernel=9):
    return cv2.bilateralFilter(frame, kernel, kernel * 2, kernel / 2)


def effect_of_whitening(frame, whiten_level=5.0, target_mask=None):
    assert 1 <= whiten_level <= 5, "whiten_level must belongs to [1, 5]"

    magic_number = 0.003921
    a = math.log(whiten_level)
    new_frame = (255 * (np.log((frame * magic_number) *
                               (whiten_level - 1) + 1) / a)).astype(np.uint8)

    if isinstance(target_mask, np.ndarray):
        return utils.get_masked_image(new_frame, target_mask)
    else:
        return new_frame


def effect_of_whitening_with_neural_network(frame, target_mask=None):
    global whitening_model
    if whitening_model is None:
        whitening_model = useWhiteningModel()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # cv2 pixel is [b, g, r] by default, we want to give it a reverse first
    rgb_input = frame[:, :, ::-1]
    rgb_input = rgb_input.reshape(-1, 3)
    rgb_output = whitening_model.predict(rgb_input)

    frame = rgb_output.reshape(frame.shape)
    frame = frame[:, :, ::-1]

    frame[frame > 255] = 255
    frame = frame.astype(np.uint8)

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # try to ignore rgb=0,0,0 if possible

    if isinstance(target_mask, np.ndarray):
        return utils.get_masked_image(frame, target_mask)
    else:
        return frame


def effect_of_whitening_with_a_top_layer(frame, target_mask=None):
    white = effect_of_pure_white(frame)
    frame = cv2.addWeighted(white, 0.2, frame, 0.85, 0)
    if isinstance(target_mask, np.ndarray):
        return utils.get_masked_image(frame, target_mask)
    else:
        return frame


def effect_of_pure_white(frame):
    white = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    white.fill(255)
    return white


def effect_of_oil_painting(frame):
    PIL_image = utils.opencv_frame_to_PIL_image(frame)
    PIL_image = oil_painting(PIL_image, 8, 255)
    frame = utils.PIL_image_to_opencv_frame(PIL_image)
    return frame


def effect_of_adding_a_mask_to_face(frame, mask_image=None):
    if not isinstance(mask_image, np.ndarray):
        mask_image = utils.read_image_as_a_frame(os.path.join(
            utils.STATIC_DIR, "mask.png"), with_transparency=True)

    self = my_dlib
    current_frame = frame
    try:
        result = my_dlib.add_a_mask_to_face(frame, mask_image)
        self.last_frame = result
    except Exception as e:
        print(e)
        if (self.last_frame.size != 0):
            result = self.last_frame
        else:
            white = np.zeros(
                (current_frame.shape[0], current_frame.shape[1], 3), dtype=np.uint8)
            white.fill(255)
            result = white

    return result


def effect_of_face_swapping(target_image, new_face=None):
    if not isinstance(new_face, np.ndarray):
        new_face = utils.read_image_as_a_frame(os.path.join(
            utils.STATIC_DIR, "mask.png"), with_transparency=False)

    self = my_dlib
    current_frame = target_image

    try:
        result = my_dlib.face_swap(target_image, new_face)
        self.last_frame = result
    except Exception as e:
        print(e)
        if (self.last_frame.size != 0):
            result = self.last_frame
        else:
            white = np.zeros(
                (current_frame.shape[0], current_frame.shape[1], 3), dtype=np.uint8)
            white.fill(255)
            result = white

    return result


def effect_of_face_slimming(source_img):
    self = my_dlib
    current_frame = source_img

    try:
        result = my_dlib.face_slimming(source_img)
    except Exception as e:
        print(e)
        self = my_dlib
        if (self.last_frame.size != 0):
            result = self.last_frame
        else:
            white = np.zeros(
                (current_frame.shape[0], current_frame.shape[1], 3), dtype=np.uint8)
            white.fill(255)
            result = white

    return result


print("effects.py was loaded.")