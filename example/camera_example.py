import sys 
sys.path.append('..')

import pornstar
import cv2


def my_handler(frame):
    cv2.imshow("src", frame)
    frame = pornstar.stylize_the_whole_image(frame, [pornstar.effect_of_whitening, pornstar.effect_of_blur_for_skin])
    return frame


pornstar.process_camera(0, my_handler)
