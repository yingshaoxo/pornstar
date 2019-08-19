from ._main import (
    terminal,
    read_image_as_a_frame,
    combine_two_frame,
    display,
    save_a_frame_as_an_image,
    get_masked_image,
    get_human_and_background_masks_from_a_frame,
    stylize_background,
    stylize_human_body,
    stylize_background_and_human_body,
    stylize_the_whole_image,
    effect_of_blur,
    effect_of_blur_for_skin,
    effect_of_whitening,
    effect_of_whitening_with_neural_network,
    effect_of_whitening_with_a_top_layer,
    effect_of_pure_white,
    effect_of_oil_painting,
    effect_of_adding_a_mask_to_face,
    process_video,
    process_camera,
)

try:
    from ._main import MyDeepLab
except Exception as e:
    print(e)

try:
    from ._main import MyDlib
except Exception as e:
    print(e)


#from ._main import *
