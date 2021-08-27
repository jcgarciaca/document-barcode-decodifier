import cv2
import numpy as np
from PIL import Image

def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)


img = cv2.imread('cedulas_test/barcode2.png', 0)
img = cv2.equalizeHist(img)

img = Image.fromarray(img)
img = change_contrast(img, 80)

img.save('cedulas_test/contrast2.png')