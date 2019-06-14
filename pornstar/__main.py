# coding: utf-8

from .__coco import CocoConfig as __CocoConfig
from .__model import MaskRCNN as __MaskRCNN
from .__utils import download_trained_weights as __download_trained_weights

import os
import cv2

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

    # Directory of images to run detection on
    IMAGE_DIR = os.path.join(ROOT_DIR, "images")

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


def get_human_and_background_from_a_frame(frame):
    results = model.detect([frame], verbose=0)
    r = results[0]
    #visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], r['scores'])

    if (r['class_ids'] == __class_names.index("person")):
        mask1 = r['masks'] == True  # non black pixel, human shape
        mask2 = r['masks'] == False  # black pixel, non-human shape

        #print(f"frame shape: {frame.shape}\nmask1 shape: {mask1.shape}\nbackgound shape: {backgound.shape}\nmask2 shape: {mask2.shape}\n\n")

        if ((frame.shape[:2] == mask1.shape[:2]) and (backgound.shape[:2] == mask2.shape[:2])):
            if ((mask1.shape[2] == 1) or (mask2.shape[2] == 1)):
                human_pixels = frame*mask1
                background_pixels = frame*mask2
                return human_pixels, background_pixels

    return None, None


def handle_frame(frame):
    pass
