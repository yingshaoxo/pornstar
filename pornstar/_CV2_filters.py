import cv2
import numpy as np
#import scipy.stats as stats
import matplotlib.pyplot as plt


def brightness_contrast(img, alpha=1.0, beta=0):
    img_contrast = img * (alpha)
    img_bright = img_contrast + (beta)
    img_bright = np.clip(img_bright, 0, 255)
    img_bright = img_bright.astype(np.uint8)
    return img_bright


def hue_saturation(img_rgb, alpha=1, beta=1):
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)
    hue = img_hsv[:, :, 0]
    saturation = img_hsv[:, :, 1]
    hue = np.clip(hue * alpha, 0, 179)
    saturation = np.clip(saturation * beta, 0, 255)
    img_hsv[:, :, 0] = hue
    img_hsv[:, :, 1] = saturation
    img_transformed = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
    return img_transformed


def grayscale(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img_gray


def vignette(img, r, g, b, a):
    color = img.copy()
    color[:, :, 0] = b
    color[:, :, 1] = g
    color[:, :, 2] = r
    res = cv2.addWeighted(img, 1-a, color, a, 0)
    return res


def replace_color(img, hl=0, sl=0, vl=0, hu=0, su=0, vu=0, nred=0, ngreen=0, nblue=0):
    rows, cols = img.shape[:2]
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # define range of color in HSV
    lower = np.array([hl, sl, hu])
    upper = np.array([hu, su, vu])
    # Threshold the HSV image to get only blue colors
    color = cv2.inRange(hsv, lower, upper)
    # Replace color
    img[color > 0] = (nblue, ngreen, nred)
    return img


def increase_channel(img, channel, increment):
    img_channel = img[:, :, channel]
    img_channel = img_channel + increment
    img_channel = np.clip(img_channel, 0, 255)
    img[:, :, channel] = img_channel
    return img


def _1977(img, hue=1, saturation=1.3, contrast=1.1, brightness=-30):
    img = hue_saturation(img, hue, saturation)
    img = brightness_contrast(img, contrast, brightness)
    img = vignette(img, 243, 106, 188, 0.3)
    return img


def Nashville(img, hue=1, saturation=1.5, contrast=1.2, brightness=10):
    img = hue_saturation(img, hue, saturation)
    img = brightness_contrast(img, contrast, brightness)
    img = replace_color(img, 0, 0, 0, 0, 0, 30, 34, 43, 109)
    img = replace_color(img, 0, 0, 200, 0, 0, 255, 247, 218, 174)
    #img = vignette(img,247,218,174,0.2)
    return img


def Toaster(img, hue=1, saturation=0.9, contrast=1.4, brightness=-20):
    img = replace_color(img, 0, 0, 0, 0, 0, 128, 51, 0, 0)
    img = replace_color(img, 150, 255, 50, 170, 255, 128, 51, 0, 0)
    img = hue_saturation(img, hue, saturation)
    img = brightness_contrast(img, contrast, brightness)
    #img = vignette(img,128,128,128,0.2)
    img = vignette(img, 255, 99, 66, 0.1)
    img = vignette(img, 250, 250, 0, 0.3)
    return img


def Kelvin(img, hue=1.2, saturation=1.5, contrast=1.3, brightness=10):
    img = hue_saturation(img, hue, saturation)
    img = brightness_contrast(img, contrast, brightness)
    img = vignette(img, 240, 240, 0, 0.1)
    return img


def Clarendon(img, hue=1, saturation=1.25, contrast=1.2, brightness=-30):
    img = hue_saturation(img, hue, saturation)
    img = brightness_contrast(img, contrast, brightness)

    return img


def Amaro(img, hue=1.1, saturation=1.5, contrast=0.9, brightness=10):
    img = hue_saturation(img, hue, saturation)
    img = brightness_contrast(img, contrast, brightness)

    return img


def Gingham(img, hue=1.1, saturation=0.9, contrast=1.1, brightness=-20):
    img = hue_saturation(img, hue, saturation)
    img = brightness_contrast(img, contrast, brightness)

    return img


def Reyes(img, hue=1.2, saturation=0.75, contrast=0.9, brightness=10):
    img = hue_saturation(img, hue, saturation)
    img = brightness_contrast(img, contrast, brightness)

    return img


def Inkwell(img, hue=1, saturation=1, contrast=1.3, brightness=-30):
    img = hue_saturation(img, hue, saturation)
    img = brightness_contrast(img, contrast, brightness)
    img = grayscale(img)
    return img


def Original(img, hue=1, saturation=1, contrast=1, brightness=0):
    img = hue_saturation(img, hue, saturation)
    img = brightness_contrast(img, contrast, brightness)
    return img
