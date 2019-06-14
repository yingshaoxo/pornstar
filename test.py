from pornstar import *

frame = read_img_as_a_frame("./girl.png")
person, background = get_human_and_background_from_a_frame(frame)
background = oil_painting_effect(background)
#display_a_frame(background)

#background = blur_a_frame(background, 25)
frame = combine_two_frame(person, background)
#display_a_frame(frame)
save_a_frame_as_an_img(terminal.fix_path("~/Desktop/girl.png"), ssrame)
