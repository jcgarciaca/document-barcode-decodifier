import cv2
import numpy as np
from PIL import Image, ImageEnhance

def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)


img = cv2.imread('cedulas_test/barcode7.png', 0)
img = cv2.equalizeHist(img)

img = Image.fromarray(img)

enhancer = ImageEnhance.Sharpness(img)
factor = 2.0
img = enhancer.enhance(factor)

enhancer = ImageEnhance.Contrast(img)
factor = 1.2
img = enhancer.enhance(factor)

img.save('cedulas_test/bar_7.png')


#cv2.imwrite('cedulas_test/bar_5.png', img)

#img = Image.fromarray(img)
#img = change_contrast(img, 60)
#img.save('cedulas_test/bar_7.png')