# coding: utf-8

from .__coco import CocoConfig as __CocoConfig
from .__model import MaskRCNN as __MaskRCNN
from .__utils import download_trained_weights as __download_trained_weights
from .__PIL_filters import oil_painting

import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from auto_everything.base import Terminal
terminal = Terminal()

# Root directory of the project
ROOT_DIR = os.path.abspath(terminal.fix_path("~/Pornstar"))
# Root directory of the project
if not terminal.exists(ROOT_DIR):
    terminal.run(f"mkdir {ROOT_DIR}")


class __InferenceConfig(__CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


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


def __opencv_frame_to_PIL_img(frame):
    img = Image.fromarray(frame)
    return img


def __PIL_img_to_opencv_frame(pil_img):
    numpy_img = np.asarray(pil_img)
    numpy_img = cv2.cvtColor(numpy_img, cv2.COLOR_BGR2RGB)
    return numpy_img[:, :, :3]


def get_human_and_background_from_a_frame(frame):
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
                human_pixels = frame*mask1
                background_pixels = frame*mask2
                return human_pixels, background_pixels

    return None, None


def read_img_as_a_frame(path_of_img):
    raw = cv2.imread(path_of_img)
    return cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)


def display_a_frame(frame):
    #plt.title('Made by yingshaoxo')
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    plt.imshow(frame)
    plt.xticks([]), plt.yticks([])
    plt.show()


def save_a_frame_as_an_img(path_of_img, frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imwrite(path_of_img, frame)


def blur_a_frame(frame, degree=20, method=1):
    if method == 1:
        return cv2.blur(frame, (degree, degree))
    elif method == 2:
        return cv2.GaussianBlur(frame, (degree, degree), 0)
    elif method == 3:
        return cv2.medianBlur(frame, degree)


def oil_painting_effect(frame):
    PIL_img = __opencv_frame_to_PIL_img(frame)
    PIL_img = oil_painting(PIL_img, 8, 255)
    frame = __PIL_img_to_opencv_frame(PIL_img) 
    return frame


def combine_two_frame(frame1, frame2):
    print(frame1.shape)
    print(frame2.shape)
    return cv2.add(frame1, frame2)
