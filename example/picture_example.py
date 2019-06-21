import sys 
sys.path.append('..')

import pornstar

file_name = "girl"
input_img = f"./{file_name}.png"
output_img = f"~/Desktop/{file_name}.png"

frame = pornstar.read_image_as_a_frame(input_img)

frame = pornstar.stylize_background(
    frame,
    stylize_function=pornstar.effect_of_blur
)

pornstar.display_a_frame(frame)
pornstar.save_a_frame_as_an_image(
    pornstar.terminal.fix_path(output_img),
    frame
)
