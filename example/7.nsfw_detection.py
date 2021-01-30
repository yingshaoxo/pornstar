import sys 
sys.path.append('..')

import pornstar

girl = pornstar.utils.read_image_as_a_frame("./girl.jpg")
couple = pornstar.utils.read_image_as_a_frame("./couple.png")

detector = pornstar.store.nsfw_detector

print(detector.detect(girl))
print(detector.isPorn(couple))
