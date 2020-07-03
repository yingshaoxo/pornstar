import sys 
sys.path.append('..')

import pornstar

def handle_frame(frame):
    frame = pornstar.effect_of_whitening(frame, whiten_level=5)
    frame = pornstar.effect_of_whitening(frame, whiten_level=5)
    return pornstar.effect_of_adding_a_mask_to_face(frame)

pornstar.process_camera(0, handle_frame)
