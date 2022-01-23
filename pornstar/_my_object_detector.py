import tensorflow as tf

import tensorflow_hub as hub

# For downloading the image.
import matplotlib.pyplot as plt
import tempfile
from six.moves.urllib.request import urlopen
from six import BytesIO

# For drawing onto the image.
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

# For measuring the inference time.
import time
import os
import cv2
import re

from . import utils


def getLabelDict():
    labelFile = os.path.join(utils.STATIC_DIR, "mscoco_label_map.pbtxt")
    with open(labelFile, "r") as f:
        text = f.read()
    ids = re.findall(r"id: (\d+)", text)
    names = re.findall(r"display_name: \"(.+)\"", text)
    labelDict = dict()
    for i, name in zip(ids, names):
        labelDict[int(i)] = name
    return labelDict


labelDict = getLabelDict()


def display_image(image):
    fig = plt.figure(figsize=(20, 15))
    plt.grid(False)
    plt.imshow(image)


def download_and_resize_image(url, new_width=256, new_height=256,
                              display=False):
    _, filename = tempfile.mkstemp(suffix=".jpg")
    response = urlopen(url)
    image_data = response.read()
    image_data = BytesIO(image_data)
    pil_image = Image.open(image_data)
    pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
    pil_image_rgb = pil_image.convert("RGB")
    pil_image_rgb.save(filename, format="JPEG", quality=90)
    print("Image downloaded to %s." % filename)
    if display:
        display_image(pil_image)
    return filename


def draw_bounding_box_on_image(image,
                               ymin,
                               xmin,
                               ymax,
                               xmax,
                               color,
                               font,
                               thickness=4,
                               display_str_list=()):
    """Adds a bounding box to an image."""
    draw = ImageDraw.Draw(image)
    im_width, im_height = image.size
    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                  ymin * im_height, ymax * im_height)
    draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
               (left, top)],
              width=thickness,
              fill=color)

    # If the total height of the display strings added to the top of the bounding
    # box exceeds the top of the image, stack the strings below the bounding box
    # instead of above.
    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    # Each display_str has a top and bottom margin of 0.05x.
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

    if top > total_display_str_height:
        text_bottom = top
    else:
        text_bottom = top + total_display_str_height
    # Reverse list and print from bottom to top.
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05 * text_height)
        draw.rectangle([(left, text_bottom - text_height - 2 * margin),
                        (left + text_width, text_bottom)],
                       fill=color)
        draw.text((left + margin, text_bottom - text_height - margin),
                  display_str,
                  fill="black",
                  font=font)
        text_bottom -= text_height - 2 * margin


def draw_boxes(image, boxes, class_names, scores, max_boxes=10, min_score=0.1):
    """Overlay labeled boxes on an image with formatted scores and label names."""
    colors = list(ImageColor.colormap.values())

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf",
                                  25)
    except IOError:
        print("Font not found, using default font.")
        font = ImageFont.load_default()

    scores = scores[0]
    class_names = class_names[0]
    boxes = boxes[0]
    for i in range(min(boxes.shape[0], max_boxes)):
        if scores[i] >= min_score:
            ymin, xmin, ymax, xmax = tuple(boxes[i])
            display_str = "{}: {}%".format(labelDict[int(class_names[i])],
                                           int(100 * scores[i]))
            color = colors[hash(class_names[i]) % len(colors)]
            image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
            draw_bounding_box_on_image(
                image_pil,
                ymin,
                xmin,
                ymax,
                xmax,
                color,
                font,
                display_str_list=[display_str])
            np.copyto(image, np.array(image_pil))
    return image


"""
scores:  [[0.7946873  0.6890771  0.6887133  0.64978445 0.6489403  0.6433085
  0.6380218  0.6093764  0.5779141  0.5365125  0.48453808 0.47063315
  0.21925223 0.2174837  0.21696082 0.21397015]]
class_names:  [[ 1.  1. 38.  1. 38.  1.  1. 38. 38.  1.  1.  1.  1.  1. 38. 16.  1. 38.
   1.  1.  1. 16. 42.  1. 38.  1. 16. 16. 38.  1. 16. 35.  1. 38. 38. 42.
   1. 37. 36. 35. 16.  1.  1.  1. 31. 35.]]
boxes:  [[[0.55928797 0.39158955 0.59213775 0.41065833]
  [0.57276475 0.0394716  0.6207652  0.05971692]
  [0.8557487  0.10840849 0.8934024  0.14938967]
  [0.4391509  0.22242013 0.47028843 0.24374893]
  [0.48920542 0.18306227 0.50563705 0.19711225]
  [0.41484687 0.5584316  0.4303085  0.5709957 ]
  [0.6980128  0.08214249 0.8094177  0.12144154]
  [0.57276475 0.0394716  0.6207652  0.05971692]]]
"""


class MyObjectDetector():
    def __init__(self):
        url = "https://github.com/yingshaoxo/pornstar/raw/master/models/ssd_mobilenet_v2_2.tar.gz"
        compressedFile = os.path.join(utils.ROOT_DIR, "ssd_mobilenet_v2_2.tar.gz")
        if not utils.disk.exists(compressedFile):
            print("downloading...")
            utils.network.download(url, compressedFile)
        localModelFolder = os.path.join(utils.ROOT_DIR, "objectDetector")
        modelPath = os.path.join(localModelFolder, "saved_model.pb")
        if not utils.disk.exists(modelPath):
            utils.disk.uncompress(compressedFile, localModelFolder)
        # module_handle = "https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2"  # @param ["https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1", "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"]
        # self.detector = hub.load(module_handle)  # .signatures['default']
        self.detector = hub.load(localModelFolder)  # .signatures['default']

    def load_img_from_url(self, path):
        img = tf.io.read_file(path)
        img = tf.image.decode_jpeg(img, channels=3)
        return img

    def load_img(self, image):
        # image = bgr2rgb(image)
        image = cv2.resize(image, None, fx=0.5, fy=0.5)
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        return tf.convert_to_tensor(image, dtype=tf.uint8)

    def detectAndDisplay(self, image):
        img = self.load_img(image)

        converted_img = tf.image.convert_image_dtype(img, tf.uint8)[tf.newaxis, ...]
        result = self.detector(converted_img)

        result = {key: value.numpy() for key, value in result.items()}

        image_with_boxes = draw_boxes(
            img.numpy(), result["detection_boxes"],
            result["detection_classes"], result["detection_scores"])

        utils.display(image_with_boxes)

    def detectAndReturnImage(self, image):
        img = self.load_img(image)

        converted_img = tf.image.convert_image_dtype(img, tf.uint8)[tf.newaxis, ...]
        result = self.detector(converted_img)

        result = {key: value.numpy() for key, value in result.items()}

        image_with_boxes = draw_boxes(
            img.numpy(), result["detection_boxes"],
            result["detection_classes"], result["detection_scores"])

        return image_with_boxes

    def detect(self, image, min_score=0.3):
        img = self.load_img(image)

        converted_img = tf.image.convert_image_dtype(img, tf.uint8)[tf.newaxis, ...]
        result = self.detector(converted_img)

        result = {key: value.numpy() for key, value in result.items()}

        scores = result["detection_scores"][0]
        class_names = result["detection_classes"][0]
        boxes = result["detection_boxes"][0]

        myClassList = []
        myScroreList = []
        myPositionList = []
        for i in range(boxes.shape[0]):
            if scores[i] >= min_score:
                myClassList.append(labelDict[int(class_names[i])])
                myScroreList.append(int(100 * scores[i]))
                # ymin, xmin, ymax, xmax = tuple(boxes[i])
                myPositionList.append(tuple(boxes[i]))

        return myClassList, myScroreList, myPositionList

    def old_run_detector(self, detector, path):
        img = self.load_img_from_url(path)

        converted_img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
        start_time = time.time()
        result = detector(converted_img)
        end_time = time.time()

        result = {key: value.numpy() for key, value in result.items()}

        print("Found %d objects." % len(result["detection_scores"]))
        print("Inference time: ", end_time - start_time)

        image_with_boxes = draw_boxes(
            img.numpy(), result["detection_boxes"],
            result["detection_class_entities"], result["detection_scores"])

        display_image(image_with_boxes)
