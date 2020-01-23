#!/usr/bin/python3

import cv2
import numpy as np
import pytesseract
from PIL import Image
from pytesseract import image_to_string
import os
import sys
from imutils.object_detection import non_max_suppression


def helper():
    print('Usage: %s png_image (by default: basic.png)' % sys.argv[0])
    exit(0)


def expiration_detection(img_path):
    # read image from the path
    image = cv2.imread(img_path)
    original_image = image.copy()
    (height, width) = image.shape[:2]

    # set the new width and height
    (new_width, new_height) = (320, 320)
    resized_width = width / float(new_width)
    resized_height = height / float(new_height)

    # resize the image
    image = cv2.resize(image, (new_width, new_height))
    (height, width) = image.shape[:2]

    # two EAST layers: probability, geometry of the area
    layers = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]
    # load EAST detector (tensorflow library)
    net = cv2.dnn.readNet('../frozen_east_text_detection.pb')
    blob = cv2.dnn.blobFromImage(image, 1.0, (width, height), (255, 255, 255), swapRB=True, crop=False)
    net.setInput(blob)
    (proba, geometry) = net.forward(layers)
    (rows, cols) = proba.shape[2:4]
    rects = []
    confidences = []

    for y in range(0, rows):
        proba_value = proba[0, 0, y]
        x_data0 = geometry[0, 0, y]
        x_data1 = geometry[0, 1, y]
        x_data2 = geometry[0, 2, y]
        x_data3 = geometry[0, 3, y]
        angles_data = geometry[0, 4, y]
        for x in range(0, cols):
            if proba_value[x] < 0.5:
                continue
            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            # extract the rotation angle for the prediction
            angle = angles_data[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # height and width of the box
            h = x_data0[x] + x_data2[x]
            w = x_data1[x] + x_data3[x]
            end_x = int(offsetX + (cos * x_data1[x]) + (sin * x_data2[x]))
            end_y = int(offsetY - (sin * x_data1[x]) + (cos * x_data2[x]))
            start_x = int(end_x - w)
            start_y = int(end_y - h)
            rects.append((start_x, start_y, end_x, end_y))
            confidences.append(proba_value[x])

    # non maximum suppression avoids to get multiple rectangles in the same area !
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # loop over the bounding boxes
    for (start_x, start_y, end_x, end_y) in boxes:
        # scale the bounding box coordinates based on the ratios
        start_x = int(start_x * resized_width)
        start_y = int(start_y * resized_height)
        end_x = int(end_x * resized_width)
        end_y = int(end_y * resized_height)

        roi = original_image[start_y:end_y, start_x:end_x]
        config = "-l eng --oem 1 --psm 7"
        text = pytesseract.image_to_string(roi, config=config)
        print(text)

        crop_img = original_image[start_y:end_y, start_x:end_x]

        # draw green box around the text found
        # cv2.rectangle(original_image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

    # show the output image
    """cv2.imshow("Text Detection", original_image)
    cv2.waitKey(0)"""


expiration_detection(sys.argv[1])
