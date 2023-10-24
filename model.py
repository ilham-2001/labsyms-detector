from constant import PATH_TO_SAVED_MODEL
from constant import CLASSES
import tensorflow as tf
import cv2 as cv
import numpy as np

HEIGHT, WIDTH = (320, 320)

APD_detector = tf.saved_model.load(PATH_TO_SAVED_MODEL)


def im_to_tensor(im):
    im_arr = cv.cvtColor(im, cv.COLOR_BGR2RGB)
    im_arr = cv.resize(im_arr, (320, 320))

    input_tensor = tf.convert_to_tensor(im_arr)
    input_tensor = input_tensor[tf.newaxis, ...]

    return im_arr, APD_detector(input_tensor)


def detect_object(im):
    im_arr, detections = im_to_tensor(im)
    dets = np.where(detections["detection_scores"][0] >= .5)[0]
    is_mask, is_coat, is_gloves = False, False, False

    for i in dets:
        ymin, xmin, ymax, xmax = detections["detection_boxes"][0][i]
        raw_label = int(detections["detection_classes"][0][i].numpy())
        score = np.round(detections["detection_scores"][0][i].numpy() * 100, 1)
        label = CLASSES[raw_label]
        (left, right, top, bottom) = (
            xmin*WIDTH, xmax*WIDTH, ymin*HEIGHT, ymax*HEIGHT)
        cv.rectangle(im_arr, (int(left), int(top)),
                     (int(right), int(bottom)), (0, 255, 0), 2)
        label_pos = (int(left), int(top)-20)
        cv.putText(im_arr, f"Class: {label}", label_pos,
                   cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
        cv.putText(im_arr, f"Confidence: {score}%", (
            label_pos[0], label_pos[1] + 15), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
            
        if label == "coat":
            is_coat = not is_coat
        elif label == "mask":
            is_mask = not is_mask
        elif label == "gloves":
            is_gloves = not is_gloves

    return cv.cvtColor(im_arr, cv.COLOR_RGB2BGR), (is_gloves, is_mask, is_coat)


def create_boundingbox(im):
    bb = {}

    _, detections = im_to_tensor(im)
    dets_index = np.where(detections["detection_scores"][0] >= .5)[0]

    for i in dets_index:
        ymin, xmin, ymax, xmax = detections["detection_boxes"][0][i]
        raw_label = int(detections["detection_classes"][0][i].numpy())
        score = np.round(detections["detection_scores"][0][i].numpy() * 100, 1)
        (left, right, top, bottom) = (
            int(xmin*WIDTH), int(xmax*WIDTH), int(ymin*HEIGHT), int(ymax*HEIGHT))

        bb[f"detection_{i}"] = {
            "label": CLASSES[raw_label],
            "score": score,
            "pos": [left, right, top, bottom]
        }

    return bb
