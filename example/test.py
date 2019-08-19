import sys 
sys.path.append('..')

import pornstar

input_img = f"./me.jpg"

raw = pornstar.read_image_as_a_frame(input_img)

frame = raw

def handle_frame(frame):
    return pornstar.effect_of_adding_a_mask_to_face(frame)

frame = pornstar.effect_of_adding_a_mask_to_face(frame)

pornstar.display(
        ("me with mask", frame), 
)
