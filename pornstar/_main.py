# coding: utf-8
from ._CV2_filters import Gingham
from ._PIL_filters import oil_painting
from pathlib import Path
from moviepy.editor import VideoFileClip
import math
import matplotlib.pyplot as plt
import cv2
import os
import logging
import shutil
import urllib.request
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np

if __name__ == "__main__":
    from _my_deeplab import MyDeepLab
    from _my_dlib import MyDlib
    from utils import ROOT_DIR, STATIC_DIR
else:
    from ._my_deeplab import MyDeepLab
    from ._my_dlib import MyDlib
    from .utils import ROOT_DIR, STATIC_DIR

from tensorflow.keras.models import load_model as _keras_load_model


def _init_Whitening_model():
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


my_deeplab = MyDeepLab()
Whitening_model = _init_Whitening_model()

my_dlib = MyDlib()


def _opencv_frame_to_PIL_image(frame):
    image = Image.fromarray(frame)
    return image


def _PIL_image_to_opencv_frame(pil_image):
    numpy_image = np.asarray(pil_image)
    return numpy_image[:, :, :3]


def read_image_as_a_frame(path_of_image, with_transparency=False):
    assert os.path.exists(path_of_image), "image does not exist!"
    if with_transparency:
        frame = cv2.imread(path_of_image, cv2.IMREAD_UNCHANGED)
    else:
        frame = cv2.imread(path_of_image)
    logging.info(f"read an image: {path_of_image}")
    return frame


def combine_two_frame(frame1, frame2):
    return cv2.add(frame1, frame2)


def display(*frames):
    """
    Display a list of images in a single figure with matplotlib.

    Parameters
    ---------
    images: List of frames(np.arrays)
    """
    images = list(frames)
    cols = 1

    n_images = len(images)

    types = [isinstance(item, tuple) for item in images]
    if all(types):
        real_images = []
        titles = []
        for item in images:
            assert isinstance(item[0], str) and isinstance(
                item[1], np.ndarray), "You should give me something like (title_string, numpy_array_frame)"
            titles.append(item[0])
            real_images.append(item[1])
        images = real_images
    else:
        titles = ['Image (%d)' % i for i in range(1, n_images + 1)]

    fig = plt.figure()
    for n, (image, title) in enumerate(zip(images, titles)):
        a = fig.add_subplot(cols, np.ceil(n_images / float(cols)), n + 1)
        if image.ndim == 2:
            plt.gray()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.imshow(image)
        a.set_title(title)
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_images)
    plt.show()


def save_a_frame_as_an_image(path_of_image, frame):
    try:
        if isinstance(path_of_image, np.ndarray):
            if type(frame) == str:
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.imwrite(frame, path_of_image)
        else:
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite(path_of_image, frame)
    except Exception as e:
        print(e)
        print("Example: save_a_frame_as_an_image(path_of_image, frame)")


def get_masked_image(frame, mask):
    image = frame * mask
    return image


def get_human_and_background_masks_from_a_frame(frame):
    results = my_deeplab.predict(frame)
    results = my_deeplab.get_human_mask(results)
    if (results.size == 0):
        return None, None
    else:
        return results, np.logical_not(results)


def stylize_background(frame, stylize_function_list=None):
    if stylize_function_list == None:
        stylize_function_list = [effect_of_pure_white]

    stylized_background = frame
    for stylize_function in stylize_function_list:
        stylized_background = stylize_function(stylized_background)

    person_mask, background_mask = get_human_and_background_masks_from_a_frame(
        frame)
    if isinstance(person_mask, np.ndarray) and isinstance(background_mask, np.ndarray):
        background = get_masked_image(stylized_background, background_mask)
        person = get_masked_image(frame, person_mask)
        the_whole_img = combine_two_frame(person, background)
        return the_whole_img
    else:
        return stylized_background


def stylize_human_body(frame, stylize_function_list=None):
    if stylize_function_list == None:
        stylize_function_list = [effect_of_blur_for_skin]

    person_mask, background_mask = get_human_and_background_masks_from_a_frame(
        frame)
    if isinstance(person_mask, np.ndarray) and isinstance(background_mask, np.ndarray):
        background = get_masked_image(frame, background_mask)
        person = get_masked_image(frame, person_mask)
        for stylize_function in stylize_function_list:
            try:
                person = stylize_function(person, target_mask=person_mask)
            except TypeError as e:
                person = stylize_function(person)
        the_whole_img = combine_two_frame(person, background)
        return the_whole_img
    else:
        return frame


def stylize_background_and_human_body(frame, background_stylize_function_list=None,
                                      human_body_stylize_function_list=None):
    if background_stylize_function_list == None:
        background_stylize_function_list = [effect_of_blur]
    if human_body_stylize_function_list == None:
        human_body_stylize_function_list = [effect_of_blur_for_skin]

    stylized_background = frame
    for stylize_function in background_stylize_function_list:
        stylized_background = stylize_function(stylized_background)

    person_mask, background_mask = get_human_and_background_masks_from_a_frame(
        frame)
    if isinstance(person_mask, np.ndarray) and isinstance(background_mask, np.ndarray):
        background = get_masked_image(stylized_background, background_mask)

        person = get_masked_image(frame, person_mask)
        for stylize_function in human_body_stylize_function_list:
            try:
                person = stylize_function(person, target_mask=person_mask)
            except TypeError as e:
                person = stylize_function(person)

        the_whole_img = combine_two_frame(person, background)
        return the_whole_img
    else:
        return stylized_background


def stylize_the_whole_image(frame, stylize_function_list=None):
    if stylize_function_list == None:
        stylize_function_list = [effect_of_oil_painting]

    for stylize_function in stylize_function_list:
        frame = stylize_function(frame)

    return frame


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

    """
    height, width, _ = frame.shape
    new_frame = np.zeros((height, width, 3), np.uint8)
    for i in range(0, height):
        for j in range(0, width):
            (b, g, r) = frame[i, j]
            if (int(b) != 0) and (int(g) != 0) and (int(r) != 0):
                rr = int(255 * (math.log((r*magic_number)*(whiten_level-1)+1)/a))
                gg = int(255 * (math.log((g*magic_number)*(whiten_level-1)+1)/a))
                bb = int(255 * (math.log((b*magic_number)*(whiten_level-1)+1)/a))
                if bb > 255:
                    bb = 255
                if gg > 255:
                    gg = 255
                if rr > 255:
                    rr = 255
                new_frame[i, j] = (bb, gg, rr)
            else:
                new_frame[i, j] = (b, g, r)
    """

    if isinstance(target_mask, np.ndarray):
        return get_masked_image(new_frame, target_mask)
    else:
        return new_frame


def effect_of_whitening_with_neural_network(frame, target_mask=None):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # cv2 pixel is [b, g, r] by default, we want to give it a reverse first
    rgb_input = frame[:, :, ::-1]
    rgb_input = rgb_input.reshape(-1, 3)
    rgb_output = Whitening_model.predict(rgb_input)

    frame = rgb_output.reshape(frame.shape)
    frame = frame[:, :, ::-1]

    frame[frame > 255] = 255
    frame = frame.astype(np.uint8)

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # try to ignore rgb=0,0,0 if possible

    if isinstance(target_mask, np.ndarray):
        return get_masked_image(frame, target_mask)
    else:
        return frame


def effect_of_whitening_with_a_top_layer(frame, target_mask=None):
    white = effect_of_pure_white(frame)
    frame = cv2.addWeighted(white, 0.2, frame, 0.85, 0)
    # frame = cv2.addWeighted(white, 0.1, frame, 0.9, 0)
    if isinstance(target_mask, np.ndarray):
        return get_masked_image(frame, target_mask)
    else:
        return frame


def effect_of_pure_white(frame):
    white = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    white.fill(255)
    return white


def effect_of_oil_painting(frame):
    PIL_image = _opencv_frame_to_PIL_image(frame)
    PIL_image = oil_painting(PIL_image, 8, 255)
    frame = _PIL_image_to_opencv_frame(PIL_image)
    return frame


def effect_of_adding_a_mask_to_face(frame, mask_image=None):
    if not isinstance(mask_image, np.ndarray):
        mask_image = read_image_as_a_frame(os.path.join(
            STATIC_DIR, "mask.png"), with_transparency=True)

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
        new_face = read_image_as_a_frame(os.path.join(
            STATIC_DIR, "mask.png"), with_transparency=False)

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


def process_video(path_of_video, effect_function=None, save_to: str = None, preview: bool = False):
    def return_the_same_frame(frame):
        return frame

    if effect_function == None:
        effect_function = return_the_same_frame
    if save_to == None:
        file_ = Path(path_of_video)
        save_to = file_.with_name(file_.stem + "_modified.mp4")

    def my_effect_function(frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = effect_function(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    clip = VideoFileClip(path_of_video)
    modified_clip = clip.fl_image(effect_function)

    if preview:
        modified_clip.preview()
    else:
        modified_clip.write_videofile(save_to)


def process_video_with_time(path_of_video, effect_function=None, save_to=None, preview: bool = False):
    def return_the_same_frame(get_frame, t: float):
        return get_frame(t)

    if effect_function == None:
        effect_function = return_the_same_frame
    if save_to == None:
        file_ = Path(path_of_video)
        save_to = file_.with_name(file_.stem + "_modified.mp4")

    clip = VideoFileClip(path_of_video)
    modified_clip = clip.fl(effect_function)

    if preview:
        modified_clip.preview()
    else:
        modified_clip.write_videofile(save_to)


def process_camera(device=0, effect_function=None, show=True):
    def return_the_same_frame(frame):
        return frame

    if effect_function == None:
        effect_function = return_the_same_frame

    cap = cv2.VideoCapture(device)

    while (True):
        ret, frame = cap.read()
        frame = effect_function(frame)

        if show:
            cv2.imshow(f"yingshaoxo's camera {str(device)}", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    img = read_image_as_a_frame("../example/trump.jpg")
    mask = read_image_as_a_frame("../example/mask.jpeg")
    display(my_dlib.face_slimming(img))
