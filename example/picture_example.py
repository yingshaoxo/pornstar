import sys 
sys.path.append('..')

import pornstar

file_name = "couple"
input_img = f"./{file_name}.png"
output_img = f"~/Desktop/{file_name}.png"

raw = pornstar.read_image_as_a_frame(input_img)

frame = raw

frame1 = pornstar.stylize_the_whole_image(
            frame,
            [pornstar.effect_of_whitening_with_a_top_layer]
        )

frame2 = pornstar.stylize_the_whole_image(
            frame,
            [pornstar.effect_of_whitening]
        )

frame3 = pornstar.stylize_the_whole_image(
            frame,
            [pornstar.effect_of_whitening_with_neural_network]
        )

pornstar.display(raw, frame1, frame2, frame3)
#pornstar.save_a_frame_as_an_image(
#    pornstar.terminal.fix_path(output_img),
#    frame
#)
