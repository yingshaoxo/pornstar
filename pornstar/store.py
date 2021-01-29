from ._my_deeplab import MyDeepLab
from ._my_dlib import MyDlib
from ._my_object_detector import MyObjectDetector
from ._white_model import loadWhiteningModel
from ._nsfw_detector import loadNSFWmodel

my_deeplab = MyDeepLab()
print("deeplab loaded")

my_dlib = MyDlib()
print("dlib loaded")

my_object_detector = MyObjectDetector()
print("objectDetector loaded")

whitening_model = loadWhiteningModel()
print("whiteningModel loaded")

nsfw_detector = loadNSFWmodel()
print("nsfw detector loaded")

print("store.py was loaded.")
