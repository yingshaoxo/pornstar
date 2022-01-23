import sys 
sys.path.append('..')

import pornstar

file_name = "couple"
input_img = f"./{file_name}.png"
output_img = f"~/Desktop/{file_name}.png"

raw = pornstar.utils.read_image_as_a_frame(input_img)

frame = raw

frame1 = pornstar.stylize_background_and_human_body(
            frame,
            [pornstar.effect_of_blur],
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

pornstar.utils.display(
        ("raw", raw), 
        ("top_layer", frame1), 
        ("traditional algorithm", frame2), 
        ("neural_network", frame3)
)
