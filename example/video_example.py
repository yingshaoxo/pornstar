import sys 
sys.path.append('..')

import pornstar


def my_handler(frame):
    frame = pornstar.stylize_background(frame, [pornstar.effect_of_blur])
    #frame = pornstar.smooth_human_body(frame)
    return frame


pornstar.process_video("./demo.mp4", my_handler, "./output.mp4")
