import requests
import os
import json
import sys
import cv2

ROOT = '/home/JulioCesar/millescanner/cedulas'
IMGS_DIR = os.path.join(ROOT, 'Images')

URL1 = 'http://127.0.0.1:5000/fingerprint-id-detection'
URL2 = 'http://127.0.0.1:5000/barcode-id-detection'
URL3 = 'http://127.0.0.1:5000/barcode-id-decode'

found = []
not_found = []
for idx in range(1, 356):
    img = os.path.join(IMGS_DIR, f'IMG_{idx}.jpg')
    print('Image:', img)
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
    if resp['decode']:
        found.append(img)
    else:
        not_found.append(img)
    print('*' * 10)

print('Found: {}'.format(len(found)))
print('Not found: {}'.format(len(not_found)))