# coding: utf-8
from auto_everything.base import Terminal
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
import dlib
import bz2
import tensorflow as tf

os.environ['KERAS_BACKEND'] = 'tensorflow'

TENSORFLOW2 = 3 > int(tf.__version__[0]) > 1
if TENSORFLOW2:  # tensorflow 2.0
    if __name__ == "__main__":
        from _deeplab import Deeplabv3
    else:
        from ._deeplab import Deeplabv3

    from tensorflow.keras.models import load_model as _keras_load_model
else:
    from keras.models import load_model as _keras_load_model
    from ._coco import CocoConfig as _CocoConfig
    from ._model import MaskRCNN as _MaskRCNN
    from ._utils import download_trained_weights as _download_trained_weights
    from ._utils import download_dlib_shape_predictor as _download_dlib_shape_predictor
    from ._PIL_filters import oil_painting
    from ._CV2_filters import Gingham


terminal = Terminal()


# Static directory of this module
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
# Root directory of the project
ROOT_DIR = os.path.abspath(terminal.fix_path("~/Pornstar"))
# Root directory of the project
if not terminal.exists(ROOT_DIR):
    terminal.run(f"mkdir {ROOT_DIR}")

logging.basicConfig(filename=os.path.join(ROOT_DIR, "_main.log"),
                    level=logging.DEBUG, filemode='w', format='%(levelname)s - %(message)s')


if (TENSORFLOW2):
    class MyDeepLab():
        label_names = np.asarray([
            'background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
            'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
            'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tv'
        ])
        model = Deeplabv3(backbone='xception', OS=16)

        def predict(self, image):
            # image = np.array(Image.open(image_path)

            # Generates labels using most basic setup.  Supports various image sizes.  Returns image labels in same format
            # as original image.  Normalization matches MobileNetV2
            trained_image_width = 512
            mean_subtraction_value = 127.5

            # resize to max dimension of images from training dataset
            w, h, _ = image.shape
            ratio = float(trained_image_width) / np.max([w, h])
            resized_image = np.array(Image.fromarray(image.astype(
                'uint8')).resize((int(ratio * h), int(ratio * w))))

            # apply normalization for trained dataset images
            resized_image = (resized_image / mean_subtraction_value) - 1.

            # pad array to square image to match training imagessqueeze()
            pad_x = int(trained_image_width - resized_image.shape[0])
            pad_y = int(trained_image_width - resized_image.shape[1])
            resized_image = np.pad(
                resized_image, ((0, pad_x), (0, pad_y), (0, 0)), mode='constant')

            # do prediction
            res = self.model.predict(np.expand_dims(resized_image, 0))
            labels = np.argmax(res.squeeze(), -1)

            # remove padding and resize back to original image
            if pad_x > 0:
                labels = labels[:-pad_x]
            if pad_y > 0:
                labels = labels[:, :-pad_y]
            labels = np.array(Image.fromarray(
                labels.astype('uint8')).resize((h, w)))

            return labels

        def get_human_mask(self, labels):
            human_index = np.where(self.label_names == "person")[0]
            if (human_index.size == 0):
                return np.array([])
            else:
                human_index = human_index[0]
                human_values = (labels == human_index).astype(np.uint8)
                return np.expand_dims(human_values, axis=2)

        def scale_up_mask(self, mask, factor=1.5):
            if factor < 1:
                return mask

            old_width, old_height, _ = mask.shape
            x = int(((factor - 1) * old_width) / 2)
            y = int(((factor - 1) * old_height) / 2)

            resized_mask = cv2.resize(mask, (0, 0), fx=factor, fy=factor)
            resized_mask = np.expand_dims(resized_mask, axis=2)
            cropped_mask = resized_mask[x:x+old_width, y:y+old_height].copy()

            return cropped_mask
else:
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
        try:
            model.load_weights(COCO_MODEL_PATH, by_name=True)
        except Exception as e:
            print(e)
            print(f"you should check {COCO_MODEL_PATH}, to see if that file exists")

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


class MyDlib:
    def __init__(self):
        print("Dlib is loading")
        self.face_detector = dlib.get_frontal_face_detector()
        dlib_shape_predictor_path = os.path.join(
            ROOT_DIR, "shape_predictor_68_face_landmarks.dat")
        if not os.path.exists(dlib_shape_predictor_path):
            self.download_dlib_shape_predictor(dlib_shape_predictor_path)
        self.face_predictor = dlib.shape_predictor(
            dlib_shape_predictor_path)
        print("Dlib loading completed")

        self.last_frame = np.array([])

    def download_dlib_shape_predictor(self, save_to):
        """Download dlib shape predictor from Releases.
        """
        bz2_file = save_to + ".bz2"
        if not os.path.exists(bz2_file):
            with urllib.request.urlopen("https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2") as resp, open(bz2_file, 'wb') as out:
                shutil.copyfileobj(resp, out)
        with open(bz2_file, "rb") as stream:
            compressed_data = stream.read()
        obj = bz2.BZ2Decompressor()
        data = obj.decompress(compressed_data)
        with open(save_to, "wb") as stream:
            stream.write(data)

    def _adjust_gamma(self, image, gamma=1.0):
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")

        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)

    def add_image_to_the_top_of_another(self, background_img, top_img, x, y, overlay_size=None):
        if overlay_size is not None:
            top_img = cv2.resize(
                top_img.copy(), overlay_size)

        bg_img = background_img.copy()
        if (top_img.shape[2] == 4):  # png with transparency
            # Extract the alpha mask of the RGBA image, convert to RGB
            b, g, r, a = cv2.split(top_img)
            overlay_color = cv2.merge((b, g, r))
            # Apply some simple filtering to remove edge noise
            mask = cv2.medianBlur(a, 5)

            h, w, _ = overlay_color.shape
            roi = bg_img[y:y+h, x:x+w]
            # Black-out the area behind the logo in our original ROI
            img1_bg = cv2.bitwise_and(
                roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))
            # Mask out the logo from the logo image.
            img2_fg = cv2.bitwise_and(overlay_color, overlay_color, mask=mask)
            #img2_fg = cv2.cvtColor(img2_fg, cv2.COLOR_BGR2RGB)
            # Update the original image with our new ROI
            bg_img[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)

            return bg_img
        else:  # no transparency info, just normal image
            h, w, _ = top_img.shape
            bg_img[y:y+h, x:x+w] = top_img

            return bg_img

    def add_a_mask_to_face(self, frame, mask_image):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector(gray_frame)
        if len(faces):  # face found
            for face in faces:
                x = face.left()
                y = face.top()
                w = face.right() - x
                h = face.bottom() - y

                y = y - int(h * 0.05)
                h = int(h * 1.05)

                frame = self.add_image_to_the_top_of_another(
                    frame, mask_image, x, y, (w, h))
            self.last_frame = frame
        else:  # no face at all
            if (self.last_frame.size != 0):
                frame = self.last_frame
            else:
                white = np.zeros(
                    (frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
                white.fill(255)
                frame = white
        return frame

    def face_swap(self, original, new_face):
        def extract_index_nparray(nparray):
            index = None
            for num in nparray[0]:
                index = num
                break
            return index

        img2 = original
        img = new_face

        # decrease the size to speed up the processing
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        mask = np.zeros_like(img_gray)
        img2_new_face = np.zeros_like(img2)

        # face detection for the first image
        faces = self.face_detector(img_gray)
        if len(faces) != 1:
            raise Exception("The second image should have a face! And only one face!")
        for face in faces:
            landmarks = self.face_predictor(img_gray, face)
            landmarks_points = []
            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                landmarks_points.append((x, y))
                #cv2.circle(img, (x, y), 3, (0, 0, 255), -1) # we don't need to draw points at the face

        points = np.array(landmarks_points, np.int32)
        convexhull = cv2.convexHull(points) # caculate the face area according to a bunch of points
        #cv2.polylines(img, [convexhull], True, (255, 0, 0), 3) # draw a border line for face
        cv2.fillConvexPoly(mask, convexhull, 255) # get the mask of the first image face
        face_image_1 = cv2.bitwise_and(img, img, mask=mask) # get the first image face

        # Delaunay triangulation
        rect = cv2.boundingRect(convexhull)
        subdiv = cv2.Subdiv2D(rect)
        subdiv.insert(landmarks_points)
        triangles = subdiv.getTriangleList() # get a bunch of triangles
        triangles = np.array(triangles, dtype=np.int32) # convert it to int

        indexes_triangles = []
        for t in triangles:
            pt1 = (t[0], t[1])
            pt2 = (t[2], t[3])
            pt3 = (t[4], t[5])

            index_pt1 = np.where((points == pt1).all(axis=1))
            index_pt1 = extract_index_nparray(index_pt1)

            index_pt2 = np.where((points == pt2).all(axis=1))
            index_pt2 = extract_index_nparray(index_pt2)

            index_pt3 = np.where((points == pt3).all(axis=1))
            index_pt3 = extract_index_nparray(index_pt3)

            if index_pt1 is not None and index_pt2 is not None and index_pt3 is not None:
                triangle = [index_pt1, index_pt2, index_pt3]
                indexes_triangles.append(triangle)

        # face detection for the second image
        faces2 = self.face_detector(img2_gray)
        if len(faces2) != 1:
            #raise Exception("The first image should have at least one face!")
            raise Exception("The first image should have a face! And only one face!")
        for face in faces2:
            landmarks = self.face_predictor(img2_gray, face)
            landmarks_points2 = []
            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                landmarks_points2.append((x, y))
                #cv2.circle(img2, (x,y), 3, (0,255,0), -1) # we don't need to draw points at the face

        points2 = np.array(landmarks_points2, np.int32)
        convexhull2 = cv2.convexHull(points2) # get the area of second face by a bunch of points

        # Triangulation of both faces
        for triangle_index in indexes_triangles:
            # Triangulation of the first face
            tr1_pt1 = landmarks_points[triangle_index[0]]
            tr1_pt2 = landmarks_points[triangle_index[1]]
            tr1_pt3 = landmarks_points[triangle_index[2]]
            triangle1 = np.array([tr1_pt1, tr1_pt2, tr1_pt3], np.int32)

            rect1 = cv2.boundingRect(triangle1)
            (x, y, w, h) = rect1
            cropped_triangle = img[y: y + h, x: x + w]
            cropped_tr1_mask = np.zeros((h, w), np.uint8)

            points = np.array([[tr1_pt1[0] - x, tr1_pt1[1] - y],
                               [tr1_pt2[0] - x, tr1_pt2[1] - y],
                               [tr1_pt3[0] - x, tr1_pt3[1] - y]], np.int32)

            cv2.fillConvexPoly(cropped_tr1_mask, points, 255)
            cropped_triangle = cv2.bitwise_and(cropped_triangle, cropped_triangle,
                                               mask=cropped_tr1_mask)

            #cv2.line(img, tr1_pt1, tr1_pt2, (0, 0, 255), 2)
            #cv2.line(img, tr1_pt3, tr1_pt2, (0, 0, 255), 2)
            #cv2.line(img, tr1_pt1, tr1_pt3, (0, 0, 255), 2)

            # Triangulation of second face
            tr2_pt1 = landmarks_points2[triangle_index[0]]
            tr2_pt2 = landmarks_points2[triangle_index[1]]
            tr2_pt3 = landmarks_points2[triangle_index[2]]
            triangle2 = np.array([tr2_pt1, tr2_pt2, tr2_pt3], np.int32)

            rect2 = cv2.boundingRect(triangle2)
            (x, y, w, h) = rect2
            cropped_triangle2 = img2[y: y + h, x: x + w]
            cropped_tr2_mask = np.zeros((h, w), np.uint8)

            points2 = np.array([[tr2_pt1[0] - x, tr2_pt1[1] - y],
                                [tr2_pt2[0] - x, tr2_pt2[1] - y],
                                [tr2_pt3[0] - x, tr2_pt3[1] - y]], np.int32)


            #cv2.fillConvexPoly(cropped_tr2_mask, points2, 255)
            #cropped_triangle2 = cv2.bitwise_and(cropped_triangle2, cropped_triangle2,
            #                                    mask=cropped_tr2_mask)

            #cv2.line(img2, tr2_pt1, tr2_pt2, (0, 0, 255), 2)
            #cv2.line(img2, tr2_pt3, tr2_pt2, (0, 0, 255), 2)
            #cv2.line(img2, tr2_pt1, tr2_pt3, (0, 0, 255), 2)

            # Warp triangles
            # We convert the first image triangle to second inage triangle. warpAffine() is the key function for doing that
            points = np.float32(points)
            points2 = np.float32(points2)
            M = cv2.getAffineTransform(points, points2)
            warped_triangle = cv2.warpAffine(cropped_triangle, M, (w, h),flags=cv2.INTER_NEAREST, borderValue=(0,0,0))

            # Reconstructing destination face
            target_index = np.any(warped_triangle != [0, 0, 0], axis=-1)
            img2_new_face[y: y + h, x: x + w][target_index] = warped_triangle[target_index]

            #cv2.imshow("piece", warped_triangle) # keep press esc to see the generating process dynamiclly
            #cv2.imshow("how we generate the new face", img2_new_face)
            #cv2.waitKey(0)

        # Face swapped (putting 1st face into 2nd face)
        img2_face_mask = np.zeros_like(img2_gray)
        img2_head_mask = cv2.fillConvexPoly(img2_face_mask, convexhull2, 255)
        img2_face_mask = cv2.bitwise_not(img2_head_mask)

        img2_head_noface = cv2.bitwise_and(img2, img2, mask=img2_face_mask)

        result = cv2.add(img2_head_noface, img2_new_face)

        #(x, y, w, h) = cv2.boundingRect(convexhull2)
        #center_face2 = (int((x + x + w) / 2), int((y + y + h) / 2))
        #seamlessclone = cv2.seamlessClone(result, img2, img2_head_mask, center_face2, cv2.NORMAL_CLONE)

        (x, y, w, h) = cv2.boundingRect(img2_head_mask)
        real_new_face = img2_new_face[y: y + h, x: x + w]
        center_face2 = (int((x + x + w) / 2), int((y + y + h) / 2))
        real_new_face_mask = img2_head_mask[y: y + h, x: x + w]
        seamlessclone = cv2.seamlessClone(real_new_face, img2, real_new_face_mask, center_face2, cv2.NORMAL_CLONE) # (new_face, the_target_image, mask_of_new_face_at_target_image, the_center_point_of_new_face_at_the_target_image, cv2.MIXED_CLONE)

        #cv2.imshow("first_img", img)
        #cv2.imshow("second_img", img2)
        #cv2.imshow("second_img_head_without_face", img2_head_noface)
        #cv2.imshow("new_face", img2_new_face)
        #cv2.imshow("raw_combine", result)
        #cv2.imshow("with seamlessclone", seamlessclone)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        return seamlessclone


if (TENSORFLOW2):
    my_deeplab = MyDeepLab()
else:
    MaskRCNN_model = _init_MASK_RCNN_model()

Whitening_model = _init_Whitening_model()

my_dlib = MyDlib()


def _opencv_frame_to_PIL_image(frame):
    image = Image.fromarray(frame)
    return image


def _PIL_image_to_opencv_frame(pil_image):
    numpy_image = np.asarray(pil_image)
    # numpy_image = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2RGB)
    return numpy_image[:, :, :3]


def read_image_as_a_frame(path_of_image, with_transparency=False):
    assert os.path.exists(path_of_image), "image does not exist!"
    if with_transparency:
        frame = cv2.imread(path_of_image, cv2.IMREAD_UNCHANGED)
    else:
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
            assert isinstance(item[0], str) and isinstance(
                item[1], np.ndarray), "You should give me something like (title_string, numpy_array_frame)"
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
    if (TENSORFLOW2):
        results = my_deeplab.predict(frame)
        results = my_deeplab.get_human_mask(results)
        if (results.size == 0):
            return None, None
        else:
            #results = my_deeplab.scale_up_mask(results)
            return results, np.logical_not(results)
    else:
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
    new_frame = (255 * (np.log((frame * magic_number) *
                               (whiten_level-1) + 1) / a)).astype(np.uint8)

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


def effect_of_adding_a_mask_to_face(frame, mask_image=None):
    if not isinstance(mask_image, np.ndarray):
        mask_image = read_image_as_a_frame(os.path.join(
            STATIC_DIR, "mask.png"), with_transparency=True)

    return my_dlib.add_a_mask_to_face(frame, mask_image)


def effect_of_face_swapping(target_image, new_face=None):
    if not isinstance(new_face, np.ndarray):
        new_face = read_image_as_a_frame(os.path.join(
            STATIC_DIR, "mask.png"), with_transparency=True)

    return my_dlib.face_swap(target_image, new_face)


def process_video(path_of_video, effect_function=None, save_to=None):
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


if __name__ == "__main__":
    img1 = read_image_as_a_frame("../example/trump.jpg")
    img2 = read_image_as_a_frame("../example/me.jpg")
    my_dlib.face_swap(img1, img2)
