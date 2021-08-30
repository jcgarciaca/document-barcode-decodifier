from PIL import Image, ImageEnhance
import cv2
import numpy as np

#read the image
im = Image.open("cedulas_test/bar_7.png")

#image brightness enhancer
enhancer = ImageEnhance.Sharpness(im)

factor = 2.0 #increase contrast
im_output = enhancer.enhance(factor)

im_output.save('cedulas_test/sharpness.png')
cv2.imshow('img', np.array(im_output))
cv2.waitKey(0)
cv2.destroyAllWindows()