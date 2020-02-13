import sys 
sys.path.append('..')

import pornstar


def my_handler(frame):
    frame = pornstar.stylize_the_whole_image(frame, [
        pornstar.effect_of_face_swapping
    ])
    return frame


pornstar.process_video("./video.mp4", my_handler, "./output.mp4")
