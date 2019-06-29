# coding: utf-8

from keras.models import load_model as _keras_load_model
import urllib.request
import shutil

import dlib
import logging
from ._coco import CocoConfig as _CocoConfig
from ._model import MaskRCNN as _MaskRCNN
from ._utils import download_trained_weights as _download_trained_weights
from ._utils import download_dlib_shape_predictor as _download_dlib_shape_predictor
from ._PIL_filters import oil_painting
from ._CV2_filters import Gingham

import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import math

from moviepy.editor import VideoFileClip
from pathlib import Path

from auto_everything.base import Terminal
terminal = Terminal()


# Root directory of the project
ROOT_DIR = os.path.abspath(terminal.fix_path("~/Pornstar"))
# Root directory of the project
if not terminal.exists(ROOT_DIR):
    terminal.run(f"mkdir {ROOT_DIR}")

logging.basicConfig(filename=os.path.join(ROOT_DIR, "_main.log"),
                    level=logging.DEBUG, filemode='w', format='%(levelname)s - %(message)s')


# init dlib
face_detector = dlib.get_frontal_face_detector()
DLIB_SHAPE_PREDICTOR_PATH = os.path.join(
    ROOT_DIR, "shape_predictor_68_face_landmarks.dat")
if not os.path.exists(DLIB_SHAPE_PREDICTOR_PATH):
    _download_dlib_shape_predictor(DLIB_SHAPE_PREDICTOR_PATH)
face_predictor = dlib.shape_predictor(DLIB_SHAPE_PREDICTOR_PATH)


class _InferenceConfig(_CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    USE_MINI_MASK = False


# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
_class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
                'bus', 'train', 'truck', 'boat', 'traffic light',
                'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
                'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
                'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
                'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
                'kite', 'baseball bat', 'baseball glove', 'skateboard',
                'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
                'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
                'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
                'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
                'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
                'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
                'teddy bear', 'hair drier', 'toothbrush']


def _init_MASK_RCNN_model():
    # Directory to save logs and trained model
    MODEL_DIR = os.path.join(ROOT_DIR, "logs")

    # Local path to trained weights file
    COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
    # Download COCO trained weights from Releases if needed
    if not os.path.exists(COCO_MODEL_PATH):
        _download_trained_weights(COCO_MODEL_PATH)

    # ## Configurations
    config = _InferenceConfig()
    config.display()

    # Create model object in inference mode.
    model = _MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

    # Load weights trained on MS-COCO
    model.load_weights(COCO_MODEL_PATH, by_name=True)

    return model


def _init_Whitening_model():
    MODEL_FILE_NAME = "pornstar_whitening_model.h5"
    MODEL_PATH = os.path.join(ROOT_DIR, MODEL_FILE_NAME)

    # Download it from Releases if needed
    if not os.path.exists(MODEL_PATH):
        print(f"Start to download {MODEL_FILE_NAME}...")
        with urllib.request.urlopen("https://github.com/yingshaoxo/pornstar/raw/master/models/" + MODEL_FILE_NAME) as resp, open(MODEL_PATH, 'wb') as out:
            shutil.copyfileobj(resp, out)
        print(f"{MODEL_FILE_NAME} was downloaded!")

    model = _keras_load_model(MODEL_PATH)

    return model


MaskRCNN_model = _init_MASK_RCNN_model()
Whitening_model = _init_Whitening_model()


def _opencv_frame_to_PIL_image(frame):
    image = Image.fromarray(frame)
    return image


def _PIL_image_to_opencv_frame(pil_image):
    numpy_image = np.asarray(pil_image)
    # numpy_image = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2RGB)
    return numpy_image[:, :, :3]


def read_image_as_a_frame(path_of_image):
    assert os.path.exists(path_of_image), "image does not exist!"
    frame = cv2.imread(path_of_image)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
            assert isinstance(item[0], str) and isinstance(item[1], np.ndarray), "You should give me something like (title_string, numpy_array_frame)"
            titles.append(item[0])
            real_images.append(item[1])
        images = real_images
    else:
        titles = ['Image (%d)' % i for i in range(1, n_images + 1)]

    fig = plt.figure()
    for n, (image, title) in enumerate(zip(images, titles)):
        a = fig.add_subplot(cols, np.ceil(n_images/float(cols)), n + 1)
        if image.ndim == 2:
            plt.gray()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.imshow(image)
        a.set_title(title)
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_images)
    plt.show()


def save_a_frame_as_an_image(path_of_image, frame):
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imwrite(path_of_image, frame)


def get_masked_image(frame, mask):
    image = frame*mask
    return image


def get_human_and_background_masks_from_a_frame(frame):
    results = MaskRCNN_model.detect([frame], verbose=0)
    r = results[0]
    # visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], r['scores'])

    # print(r['class_ids'])
    if (_class_names.index("person") in r['class_ids']):
        a_tuple = np.where(r['class_ids'] == _class_names.index("person"))
        index_array = a_tuple[0]

        # print(r['masks'].shape) # The shape is strange, you should see function display_instances() in visualize.py for more details
        if len(index_array) > 0:
            logging.debug(f"index_array shape: {index_array}")
            shape = r['masks'][:, :, [0]].shape
            logging.debug(f"original frame shape: {shape}")
            final_mask1 = np.zeros((shape[0], shape[1], 1), dtype=np.uint8)
            logging.debug(f"final_mask1 size: {final_mask1.shape}")
            for index in index_array:
                mask = r['masks'][:, :, [index]]
                logging.debug(f"single mask after use index: {mask.shape}")

                # non black pixel, human shape
                mask1 = (mask == True).astype(np.uint8)
                # mask2 = (mask == False).astype(np.uint8)  # black pixel, non-human shape

                logging.debug(f"mask1.shape: {mask1.shape}")
                # cv2.bitwise_or(final_mask1, mask1)
                final_mask1 = np.logical_or(final_mask1, mask1)

            logging.debug(f"final_mask1 size: {final_mask1.shape}\n")
            return final_mask1, np.logical_not(final_mask1)

    return None, None


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
        stylize_function_list = [effect_of_blur_for_face]

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


def stylize_background_and_human_body(frame, background_stylize_function_list=None, human_body_stylize_function_list=None):
    if background_stylize_function_list == None:
        background_stylize_function_list = [effect_of_blur]
    if human_body_stylize_function_list == None:
        human_body_stylize_function_list = [effect_of_blur_for_face]

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
    return cv2.bilateralFilter(frame, kernel, kernel*2, kernel/2)


def effect_of_whitening(frame, whiten_level=5.0, target_mask=None):
    assert 1 <= whiten_level <= 5, "whiten_level must belongs to [1, 5]"

    magic_number = 0.003921
    a = math.log(whiten_level)
    new_frame = (255 * (np.log((frame * magic_number) * (whiten_level-1) + 1) / a)).astype(np.uint8)

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
    #frame = cv2.addWeighted(white, 0.1, frame, 0.9, 0)
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


def process_video(path_of_video, effect_function=None, save_to=None):
    def return_the_same_frame(frame):
        return frame

    if effect_function == None:
        effect_function = return_the_same_frame
    if save_to == None:
        file_ = Path(path_of_video)
        save_to = file_.with_name(file_.stem + "_modified.mp4")

    clip = VideoFileClip(path_of_video)
    modified_clip = clip.fl_image(effect_function)

    modified_clip.write_videofile(save_to)


def process_camera(device=0, effect_function=None, save_to=None):
    def return_the_same_frame(frame):
        return frame

    if effect_function == None:
        effect_function = return_the_same_frame

    cap = cv2.VideoCapture(device)

    while(True):
        ret, frame = cap.read()
        frame = effect_function(frame)

        cv2.imshow(f"yingshaoxo's camera {str(device)}", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
