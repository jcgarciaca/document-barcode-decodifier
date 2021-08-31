import tensorflow as tf
from object_detection.utils import label_map_util, config_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
import os
import numpy as np

class Detector:
    def __init__(self, PATH_TO_SAVED_MODEL, PATH_TO_LABELS, model_name):
        self.detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
        self.category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
        self.min_score_thresh = .8
        print(f'{model_name} loaded')


    def run_detection(self, image_np):
        result = {'found': False, 'bbox': {'xmin': None, 'xmax': None, 'ymin': None, 'ymax': None}, 'score': None}
        h, w, _ = image_np.shape
        input_tensor = tf.convert_to_tensor(image_np)
        input_tensor = input_tensor[tf.newaxis, ...]

        # run detections
        detections = self.detect_fn(input_tensor)
        num_detections = int(detections.pop('num_detections'))

        detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
        detections['num_detections'] = num_detections

        # detection_classes should be ints
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
        
        if detections['detection_scores'][0] >= self.min_score_thresh:
            result['found'] = True
            ymin, xmin, ymax, xmax = detections['detection_boxes'][0]
            ymin, xmin, ymax, xmax = int(ymin * h), int(xmin * w), int(ymax * h), int(xmax * w)
            result['bbox']['xmin'] = xmin
            result['bbox']['xmax'] = xmax
            result['bbox']['ymin'] = ymin
            result['bbox']['ymax'] = ymax
            result['score'] = round(detections['detection_scores'][0] * 100)
        return result