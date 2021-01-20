from ._main import my_dlib

def faceExists(image):
    try:
        my_dlib.get_face(image)
        return True
    except Exception as e:
        return False
