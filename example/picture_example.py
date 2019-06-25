import sys 
sys.path.append('..')

import pornstar

file_name = "couple"
input_img = f"./{file_name}.png"
output_img = f"~/Desktop/{file_name}.png"

raw = pornstar.read_image_as_a_frame(input_img)

frame = raw

frame = pornstar.stylize_background_and_human_body(
            frame,
            human_body_stylize_function_list = [pornstar.effect_of_whitening]
        )

pornstar.display(raw, frame)
pornstar.save_a_frame_as_an_image(
    pornstar.terminal.fix_path(output_img),
    frame
)
