import requests
import os
import json
import sys
import cv2

ROOT = '/home/JulioCesar/millescanner/cedulas'
IMGS_DIR = os.path.join(ROOT, 'Images')

# ROOT = os.path.dirname(os.path.realpath(__file__))
# IMGS_DIR = os.path.join(ROOT, 'test_imgs')

img = os.path.join(IMGS_DIR, sys.argv[1])
URL1 = 'http://127.0.0.1:5000/fingerprint-id-detection'
URL2 = 'http://127.0.0.1:5000/barcode-id-detection'
URL3 = 'http://127.0.0.1:5000/barcode-id-decode'


# find fingerprint
print('Fingerprint:')
files = {'image': open(img, 'rb')}
r = requests.post(URL1, files=files)
resp = r.json()
print(resp)
print('-' * 5)

# find barcode
print('Barcode:')
files = {'image': open(img, 'rb')}
r = requests.post(URL2, files=files)
resp = r.json()
print(resp)
print('-' * 5)

# decode barcode
print('Decode barcode:')
barcode_path = os.path.join(IMGS_DIR, 'barcode.jpg')
barcode = cv2.imread(img)
# crop
bbox = resp['bbox']
barcode = barcode[bbox['ymin']:bbox['ymax'], bbox['xmin']:bbox['xmax']]
cv2.imwrite(barcode_path, barcode)

files = {'barcode': open(barcode_path, 'rb')}
r = requests.post(URL3, files=files)
resp = r.json()
print(resp)