import pornstar


def my_handler(frame):
    return pornstar.stylize_background(frame, pornstar.effect_of_blur)


pornstar.process_video("./real_demo.mp4", my_handler, "./output.mp4")
