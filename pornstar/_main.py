# coding: utf-8
from pathlib import Path
from moviepy.editor import VideoFileClip

from .effects import *
from .store import *
from . import utils

my_deeplab = None


def get_human_and_background_masks_from_a_frame(frame):
    global my_deeplab
    if my_deeplab == None:
        my_deeplab = useMyDeepLab()

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
        background = utils.get_masked_image(stylized_background, background_mask)
        person = utils.get_masked_image(frame, person_mask)
        the_whole_img = utils.combine_two_frame(person, background)
        return the_whole_img
    else:
        return stylized_background


def stylize_human_body(frame, stylize_function_list=None):
    if stylize_function_list == None:
        stylize_function_list = [effect_of_blur_for_skin]

    person_mask, background_mask = get_human_and_background_masks_from_a_frame(
        frame)
    if isinstance(person_mask, np.ndarray) and isinstance(background_mask, np.ndarray):
        background = utils.get_masked_image(frame, background_mask)
        person = utils.get_masked_image(frame, person_mask)
        for stylize_function in stylize_function_list:
            try:
                person = stylize_function(person, target_mask=person_mask)
            except TypeError as e:
                person = stylize_function(person)
        the_whole_img = utils.combine_two_frame(person, background)
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
        background = utils.get_masked_image(stylized_background, background_mask)

        person = utils.get_masked_image(frame, person_mask)
        for stylize_function in human_body_stylize_function_list:
            try:
                person = stylize_function(person, target_mask=person_mask)
            except TypeError as e:
                person = stylize_function(person)

        the_whole_img = utils.combine_two_frame(person, background)
        return the_whole_img
    else:
        return stylized_background


def stylize_the_whole_image(frame, stylize_function_list=None):
    if stylize_function_list == None:
        stylize_function_list = [effect_of_oil_painting]

    for stylize_function in stylize_function_list:
        frame = stylize_function(frame)

    return frame


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


print("_main.py was loaded.")
