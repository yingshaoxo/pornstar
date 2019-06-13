
# coding: utf-8

# # Mask R-CNN Demo
# 
# A quick intro to using the pre-trained model to detect and segment objects.

# In[1]:


import os
import sys
import random
import math
import cv2
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt

# Root directory of the project
ROOT_DIR = os.path.abspath("./")

# Import Mask RCNN
from .utils import download_trained_weights
from .model import MaskRCNN
# Import COCO config
from .coco import CocoConfig

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "images")


# ## Configurations
# 
# We'll be using a model trained on the MS-COCO dataset. The configurations of this model are in the ```CocoConfig``` class in ```coco.py```.
# 
# For inferencing, modify the configurations a bit to fit the task. To do so, sub-class the ```CocoConfig``` class and override the attributes you need to change.

# In[2]:


class InferenceConfig(CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
config.display()


# ## Create Model and Load Trained Weights

# In[3]:


# Create model object in inference mode.
model = MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)


# ## Class Names
# 
# The model classifies objects and returns class IDs, which are integer value that identify each class. Some datasets assign integer values to their classes and some don't. For example, in the MS-COCO dataset, the 'person' class is 1 and 'teddy bear' is 88. The IDs are often sequential, but not always. The COCO dataset, for example, has classes associated with class IDs 70 and 72, but not 71.
# 
# To improve consistency, and to support training on data from multiple sources at the same time, our ```Dataset``` class assigns it's own sequential integer IDs to each class. For example, if you load the COCO dataset using our ```Dataset``` class, the 'person' class would get class ID = 1 (just like COCO) and the 'teddy bear' class is 78 (different from COCO). Keep that in mind when mapping class IDs to class names.
# 
# To get the list of class names, you'd load the dataset and then use the ```class_names``` property like this.
# ```
# # Load COCO dataset
# dataset = coco.CocoDataset()
# dataset.load_coco(COCO_DIR, "train")
# dataset.prepare()
# 
# # Print class names
# print(dataset.class_names)
# ```
# 
# We don't want to require you to download the COCO dataset just to run this demo, so we're including the list of class names below. The index of the class name in the list represent its ID (first class is 0, second is 1, third is 2, ...etc.)

# In[4]:


# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
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


# ## Run Object Detection

# In[5]:


def apply_mask(image, mask):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image[:, :, 0] = np.where(
        mask == 0,
        gray_image[:, :],
        image[:, :, 0]
    )
    image[:, :, 1] = np.where(
        mask == 0,
        gray_image[:, :],
        image[:, :, 1]
    )
    image[:, :, 2] = np.where(
        mask == 0,
        gray_image[:, :],
        image[:, :, 2]
    )
    return image


def display_instances(image, boxes, masks, ids, names, scores):
    # max_area will save the largest object for all the detection results
    max_area = 0

    # n_instances saves the amount of all objects
    n_instances = boxes.shape[0]

    if not n_instances:
        print('NO INSTANCES TO DISPLAY')
    else:
        assert boxes.shape[0] == masks.shape[-1] == ids.shape[0]

    for i in range(n_instances):
        if not np.any(boxes[i]):
            continue

        # compute the square of each object
        y1, x1, y2, x2 = boxes[i]
        square = (y2 - y1) * (x2 - x1)

        # use label to select person object from all the 80 classes in COCO dataset
        label = names[ids[i]]
        if label == 'person':
            # save the largest object in the image as main character
            # other people will be regarded as background
            if square > max_area:
                max_area = square
                mask = masks[:, :, i]
            else:
                continue
        else:
            continue

        # apply mask for the image
        image = apply_mask(image, mask)

    return image


# In[6]:


#input_video = 'demo/1.mp4'
input_video = 0
capture = cv2.VideoCapture(input_video)


# Recording Video
fps = 25.0
width = int(capture.get(3))
height = int(capture.get(4))
fcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
#out = cv2.VideoWriter("new_video.avi", fcc, fps, (width, height))


backgound = cv2.imread("./background.jpg")
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))   # float
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float
backgound = cv2.resize(backgound, (width, height))
last_frame = None

while True:
    ret, frame = capture.read()
    results = model.detect([frame], verbose=0)
    r = results[0]
    """
    new_frame = display_instances(
        frame, r['rois'], r['masks'], r['class_ids'], class_names, r['scores']
    )
    """

    mask1 = r['masks'] == True  # non black pixel, human shape
    mask2 = r['masks'] == False  # black pixel, non-human shape

    #print(f"frame shape: {frame.shape}\nmask1 shape: {mask1.shape}\nbackgound shape: {backgound.shape}\nmask2 shape: {mask2.shape}\n\n")

    if ((frame.shape[:2] == mask1.shape[:2]) and (backgound.shape[:2] == mask2.shape[:2])):
        if ((mask1.shape[2] == 1) or (mask2.shape[2] == 1)):
            human_pixels = frame*mask1
            #env_pixels = frame*mask2
            env_pixels = backgound*mask2
            frame = human_pixels + env_pixels
            cv2.imshow('video', frame)

    # Recording Video
    # out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

