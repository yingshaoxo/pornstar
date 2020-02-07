import sys 
sys.path.append('..')

import pornstar

target_image = "./trump.jpg"
new_face = "./me.jpg"

target_image = pornstar.read_image_as_a_frame(target_image)
new_face = pornstar.read_image_as_a_frame(new_face)

def process(frame):
    frame = pornstar.effect_of_face_swapping(frame)
    return frame

result = pornstar.stylize_the_whole_image(
            target_image,
            [process]
        )

pornstar.display(
        ("target_image", target_image), 
        ("new_face", new_face), 
        ("swapped", result), 
)
