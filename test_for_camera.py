import pornstar


def my_handler(frame):
    frame = pornstar.stylize_background(frame, pornstar.effect_of_blur)
    #frame = pornstar.smooth_human_body(frame)
    return frame


pornstar.process_camera(0, my_handler)
