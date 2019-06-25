import sys 
sys.path.append('..')

import pornstar
import cv2


def my_handler(frame):
    cv2.imshow("src", frame)
    #frame = pornstar.stylize_human_body(frame, [pornstar.effect_of_whitening, pornstar.effect_of_blur_for_face])
    #frame = pornstar.stylize_human_body(frame, [pornstar.effect_of_whitening, pornstar.effect_of_blur_for_face])
    frame = pornstar.stylize_background_and_human_body(frame, [pornstar.effect_of_blur], [pornstar.effect_of_whitening, pornstar.effect_of_blur_for_face])
    return frame


pornstar.process_camera(0, my_handler)
