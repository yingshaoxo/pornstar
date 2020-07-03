import sys 
sys.path.append('..')

import pornstar
import cv2


def my_handler(frame):
    cv2.imshow("src", frame)
    #frame = pornstar.stylize_the_whole_image(frame, [pornstar.effect_of_whitening_with_neural_network, pornstar.effect_of_blur_for_skin])
    #frame = pornstar.stylize_human_body(frame, [pornstar.effect_of_whitening_with_neural_network, pornstar.effect_of_blur_for_skin])
    frame = pornstar.stylize_background_and_human_body(
            frame,
            [pornstar.effect_of_pure_white],
            [pornstar.effect_of_whitening]
        )

    return frame


pornstar.process_camera(0, my_handler)
