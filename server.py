
from flask import Flask, request, Response
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image, ImageEnhance
import json
import os
import cv2
from object_detector import Detector
from barcode_decoder import decode_fn

ROOT = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(ROOT, 'tmp_images')

fingerprint_detector = Detector(
    PATH_TO_SAVED_MODEL=os.path.join(ROOT, 'model', 'train_1', 'ckpt-7', 'saved_model'), 
    PATH_TO_LABELS=os.path.join(ROOT, 'model', 'fingerprint_map.pbtxt'), 
    model_name='fingerprint_model'
)
barcode_detector = Detector(
    PATH_TO_SAVED_MODEL=os.path.join(ROOT, 'model', 'train_2', 'ckpt-6', 'saved_model'), 
    PATH_TO_LABELS=os.path.join(ROOT, 'model', 'barcode_map.pbtxt'), 
    model_name='barcode_model'
)

@app.route('/fingerprint-id-detection', methods=['POST'])
def fingerprint_inference():
    for file in request.files:
        image_np = np.array(Image.open(request.files[file]))
        detections = fingerprint_detector.run_detection(image_np)
    return Response(json.dumps(detections), mimetype='application/json')

@app.route('/barcode-id-detection', methods=['POST'])
def barcode_inference():
    for file in request.files:
        image_np = np.array(Image.open(request.files[file]))
        detections = barcode_detector.run_detection(image_np)
    return Response(json.dumps(detections), mimetype='application/json')

@app.route('/barcode-id-decode', methods=['POST'])
def barcode_decode():
    sharpness_lst = [2.0, 2.5, 2.6, 2.8]
    contrast_lst = [1.2, 0.5, 0.4, 1.6]
    for file in request.files:
        img = np.array(Image.open(request.files[file]))        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.equalizeHist(img)
        img = Image.fromarray(img)
        equalized_img = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], f'{file}_equalized.jpg'))
        img.save(equalized_img)

        found = False
        for sharpness, contrast in zip(sharpness_lst, contrast_lst):
            img_output = Image.open(equalized_img)
            enhancer = ImageEnhance.Sharpness(img_output)
            img_output = enhancer.enhance(sharpness)

            enhancer = ImageEnhance.Contrast(img_output)
            img_output = enhancer.enhance(contrast)

            processed_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{file}.jpg')
            img_output.save(processed_path)
            resp = decode_fn(processed_path)

            if resp['decode']:
                found = True
                break
        
        # explore
        if not found:
            for sharpness in np.arange(1.4, 3, 0.1):
                for contrast in np.arange(2, 3, 0.1):
                    img_output = Image.open(equalized_img)
                    enhancer = ImageEnhance.Sharpness(img_output)
                    img_output = enhancer.enhance(sharpness)

                    enhancer = ImageEnhance.Contrast(img_output)
                    img_output = enhancer.enhance(contrast)

                    processed_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{file}.jpg')
                    img_output.save(processed_path)
                    resp = decode_fn(processed_path)

                    if resp['decode']:
                        found = True
                        break
                if found:
                    break
    
    return Response(json.dumps(resp), mimetype='application/json')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port='5000', debug=True)