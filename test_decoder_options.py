import cv2
import numpy as np
from PIL import Image, ImageEnhance
from barcode_decoder import decode_fn
import os

def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)


src_filename = 'barcode_equalized'
src = os.path.join('cedulas_test', src_filename + '.jpg')

sharpness_lst = []
contrast_lst = []
for sharpness in np.arange(0, 3, 0.1):
    for contrast in np.arange(0, 3, 0.1):
        print('Test. sharpness: {}, contrast: {}'.format(sharpness, contrast))
        img = Image.open(src)

        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(sharpness)

        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast)

        dst = os.path.join('cedulas_test', f'{src_filename}_1.jpg')
        img.save(dst)

        resp = decode_fn(dst)
        if resp['decode']:
            sharpness_lst.append(sharpness)
            contrast_lst.append(contrast)
            print('Found. sharpness: {}, contrast: {}'.format(sharpness, contrast))
            print(resp)
        print('-' * 5)


print('sharpness:', sharpness_lst)
print()
print('contrast:', contrast_lst)
print()
print(len(sharpness_lst))
