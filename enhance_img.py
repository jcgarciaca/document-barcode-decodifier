from PIL import Image, ImageEnhance
import cv2
import numpy as np

#read the image
im_output = Image.open("cedulas_test/bar_7.png")

enhancer = ImageEnhance.Brightness(im_output)
factor = 1.5
im_output = enhancer.enhance(factor)

enhancer = ImageEnhance.Contrast(im_output)
factor = 1.2
im_output = enhancer.enhance(factor)


cv2.imshow('img', np.array(im_output))
cv2.waitKey(0)
cv2.destroyAllWindows()