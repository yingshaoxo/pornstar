import sys 
sys.path.append('..')

import pornstar

picture = pornstar.utils.read_image_as_a_frame("./beach.jpg")

detector = pornstar.store.my_object_detector
print(detector.detect(picture))
detector.detectAndDisplay(picture)
