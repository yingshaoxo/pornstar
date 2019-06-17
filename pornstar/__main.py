# coding: utf-8

import logging
from .__coco import CocoConfig as __CocoConfig
from .__model import MaskRCNN as __MaskRCNN
from .__utils import download_trained_weights as __download_trained_weights
from .__PIL_filters import oil_painting

import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import math

from auto_everything.base import Terminal
terminal = Terminal()

# Root directory of the project
ROOT_DIR = os.path.abspath(terminal.fix_path("~/Pornstar"))
# Root directory of the project
if not terminal.exists(ROOT_DIR):
    terminal.run(f"mkdir {ROOT_DIR}")

logging.basicConfig(filename=os.path.join(ROOT_DIR, "__main.log"),
                    level=logging.DEBUG, filemode='w', format='%(levelname)s - %(message)s')


class __InferenceConfig(__CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    USE_MINI_MASK = False


def init_model():
    # Import Mask RCNN
    # Import COCO config

    # Directory to save logs and trained model
    MODEL_DIR = os.path.join(ROOT_DIR, "logs")

    # Local path to trained weights file
    COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
    # Download COCO trained weights from Releases if needed
    if not os.path.exists(COCO_MODEL_PATH):
        __download_trained_weights(COCO_MODEL_PATH)

    # ## Configurations
    config = __InferenceConfig()
    config.display()

    # Create model object in inference mode.
    model = __MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

    # Load weights trained on MS-COCO
    model.load_weights(COCO_MODEL_PATH, by_name=True)

    return model


# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
__class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
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


model = init_model()


def __opencv_frame_to_PIL_image(frame):
    image = Image.fromarray(frame)
    return image


def __PIL_image_to_opencv_frame(pil_image):
    numpy_image = np.asarray(pil_image)
    #numpy_image = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2RGB)
    return numpy_image[:, :, :3]


def read_image_as_a_frame(path_of_image):
    frame = cv2.imread(path_of_image)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    logging.info(f"read an image: {path_of_image}")
    return frame


def combine_two_frame(frame1, frame2):
    return cv2.add(frame1, frame2)


def display_a_frame(frame):
    logging.debug(f"\n\ndisplay_a_frame with a shape of {frame.shape}")
    #plt.title('Made by yingshaoxo')
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    plt.imshow(frame)
    plt.xticks([]), plt.yticks([])
    plt.show()


def save_a_frame_as_an_image(path_of_image, frame):
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imwrite(path_of_image, frame)


def get_masked_image(frame, mask):
    image = frame*mask
    return image


def get_human_and_background_masks_from_a_frame(frame):
    results = model.detect([frame], verbose=0)
    r = results[0]
    # visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], r['scores'])

    # print(r['class_ids'])
    if (__class_names.index("person") in r['class_ids']):
        index = np.where(r['class_ids'] == __class_names.index("person"))

        # print(r['masks'].shape) # The shape is stange, you should see function display_instances() in visualize.py for more details
        mask = np.squeeze(r['masks'][:, :, index], axis=3)
        mask1 = (mask == True)  # non black pixel, human shape
        mask2 = (mask == False)  # black pixel, non-human shape

        #print(f"frame shape: {frame.shape}\nmask1 shape: {mask1.shape}\nbackgound shape: {backgound.shape}\nmask2 shape: {mask2.shape}\n\n")
        if (frame.shape[:2] == mask1.shape[:2] == mask2.shape[:2]):
            if ((mask1.shape[2] == 1) or (mask2.shape[2] == 1)):
                #human_pixels = frame*mask1
                #background_pixels = frame*mask2

                return mask1.astype(np.uint8), mask2.astype(np.uint8)

    return None, None


def stylize_background(frame, stylize_function=None):
    if stylize_function == None:
        stylize_function = effect_of_pure_white
    stylized_background = stylize_function(frame)
    person_mask, background_mask = get_human_and_background_masks_from_a_frame(
        frame)
    if isinstance(person_mask, np.ndarray) and isinstance(background_mask, np.ndarray):
        background = get_masked_image(stylized_background, background_mask)
        person = get_masked_image(frame, person_mask)
        the_whole_img = combine_two_frame(person, background)
        return the_whole_img
    else:
        return stylized_background


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


def effect_of_oil_painting(frame):
    PIL_image = __opencv_frame_to_PIL_image(frame)
    #PIL_image = oil_painting(PIL_image, 8, 255)
    PIL_image = oil_painting(PIL_image, 8, 255)
    frame = __PIL_image_to_opencv_frame(PIL_image)
    return frame


def effect_of_pure_white(frame):
    white = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    white.fill(255)
    return white
