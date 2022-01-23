def useMyDeepLab():
    from ._my_deeplab import MyDeepLab
    my_deeplab = MyDeepLab()
    print("deeplab loaded")
    return my_deeplab

def useMyDlib():
    from ._my_dlib import MyDlib
    my_dlib = MyDlib()
    print("dlib loaded")
    return my_dlib

def useMyObjectDetector():
    from ._my_object_detector import MyObjectDetector
    my_object_detector = MyObjectDetector()
    print("objectDetector loaded")
    return my_object_detector

def useWhiteningModel():
    from ._white_model import useWhiteningModel
    whitening_model = useWhiteningModel()
    print("whiteningModel loaded")
    return whitening_model

def useNSFWDetector():
    from ._nsfw_detector import NSFWDetector
    nsfw_detector = NSFWDetector()
    print("nsfwDetector loaded")
    return nsfw_detector

def useAudioClassifier():
    from ._audio_module import AudioClassifier
    AudioClassifier = AudioClassifier()
    return AudioClassifier

print("store.py was loaded.")