import sys 
sys.path.append('..')

import pornstar

girl = pornstar.utils.read_image_as_a_frame("./girl.jpg")
couple = pornstar.utils.read_image_as_a_frame("./couple.png")

detector = pornstar.useNSFWDetector()

print(detector.detect(girl))
print(detector.isPorn(couple))
