import sys 
sys.path.append('..')

import pornstar

picture = pornstar.utils.read_image_as_a_frame("./beach.jpg")

detector = pornstar.useMyObjectDetector()
print(detector.detect(picture))
detector.detectAndDisplay(picture)
