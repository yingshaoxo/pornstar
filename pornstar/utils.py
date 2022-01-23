from moviepy.editor import VideoFileClip
import os
from auto_everything.terminal import Terminal
from auto_everything.disk import Disk
from auto_everything.network import Network
import logging

from PIL import Image
from matplotlib import pyplot as plt
import cv2
import numpy as np

from tensorflow import keras

os.environ['KERAS_BACKEND'] = 'tensorflow'

terminal = Terminal()
disk = Disk()
network = Network()

# Static directory of this module
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
# Root directory of the project
ROOT_DIR = os.path.abspath(terminal.fix_path("~/Pornstar"))
# Root directory of the project
if not terminal.exists(ROOT_DIR):
    terminal.run(f"mkdir {ROOT_DIR}")

logging.basicConfig(filename=os.path.join(ROOT_DIR, "_main.log"),
                    level=logging.DEBUG, filemode='w', format='%(levelname)s - %(message)s')


def getVideoLength(path: str):
    clip = VideoFileClip(path)
    return clip.duration


def bgr2rgb(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def opencv_frame_to_PIL_image(frame):
    image = Image.fromarray(frame)
    return image


def PIL_image_to_opencv_frame(pil_image):
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
        a = fig.add_subplot(cols, int(np.ceil(n_images / float(cols))), n + 1)
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


print("utils.py was loaded.")
