import sys 
sys.path.append('..')

import pornstar


def my_handler(frame):
    #frame = pornstar.stylize_background(frame, [pornstar.effect_of_blur])
    frame = pornstar.stylize_the_whole_image(frame, [pornstar.effect_of_whitening])
    return frame


pornstar.process_video("./input.mp4", my_handler, "./output.mp4")
