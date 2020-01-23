#!/bin/python3

import numpy as np
import argparse
import imutils
import cv2
from pyzbar import pyzbar


def parse_arguments():
    # Useful to parse arguments (here: get image path)
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', required=False, help='Give the path to the image barcode')
    parser.add_argument('-v', '--video', required=False, help='Give the path to the video')
    parser.add_argument('-l', '--live', action='store_true', required=False, help='Live detection')

    args = vars(parser.parse_args())
    if args['image'] is None and args['video'] is None and args['live'] is False:
        print('Need --image, --video, or --live')
    elif args['live'] is True and (args['image'] is not None or args['video'] is not None):
        print('Live only, or image/video only')
    elif args['image'] is not None and args['video'] is not None:
        print('Give only image or video')
    else:
        return args
    return None


def crop_image(image, rect):
    center, size, angle = rect[0], rect[1], rect[2]
    center, size = tuple(map(int, center)), tuple(map(int, size))

    # get size of the image
    height, width = image.shape[0], image.shape[1]
    # enlarge zone of detection
    size = (size[0] + int(width * 0.1), size[1] + int(height * 0.1))

    # calculate the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1)

    # rotate the original image to adjust the barcode position
    image_rotated = cv2.warpAffine(image, M, (width, height))
    img_cropped = cv2.getRectSubPix(image_rotated, size, center)
    return img_cropped


def extract_barcode(image):
    barcodes = pyzbar.decode(image)
    data = []

    # in case we find multiple barcodes in the image
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect

        barcode_id = barcode.data.decode("utf-8")
        type = barcode.type

        # print the barcode type and data to the terminal
        print("Found {} barcode: {}".format(type, barcode_id))
        data.append(barcode_id)
    return data


def decode_img(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # scharr gradient: increase intensity black & white to improve detection of the edges of the barcode
    if imutils.is_cv2():
        ddepth = cv2.cv.CV_32F
    else:
        ddepth = cv2.CV_32F
    grad_x = cv2.Sobel(gray_image, ddepth=ddepth, dx=1, dy=0, ksize=-1)
    grad_y = cv2.Sobel(gray_image, ddepth=ddepth, dx=0, dy=1, ksize=-1)
    gradient = cv2.subtract(grad_x, grad_y)
    gradient = cv2.convertScaleAbs(gradient)

    # blur the image to get only the white part of the image: the barcode (approximation)
    blur = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blur, 225, 255, cv2.THRESH_BINARY)

    # remove gaps: the goal is to make the zone fully white
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)

    # find the contours in the image
    contours = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    # sort contours by x / y to get them in the right order
    if contours is None or len(contours) == 0:
        return []
    c = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    if imutils.is_cv2():
        box = cv2.cv.BoxPoints(rect)
    else:
        box = cv2.boxPoints(rect)
    box = np.int0(box)

    # draw a bounding box arounded the detected barcode and display the
    # image
    image_cpy = image.copy()
    cv2.drawContours(image_cpy, [box], -1, (0, 255, 0), 3)

    img_cropped = crop_image(image, rect)
    data = extract_barcode(img_cropped)
    return data


def decode_video(args):
    video = cv2.VideoCapture(args['video'])
    if video is None or not video.isOpened():
        print('Wrong format file')
        exit(1)

    success, image = video.read()
    fps = video.get(cv2.CAP_PROP_FPS)
    rate = 0
    data = []

    while success:
        frame_id = int(round(video.get(1)))
        data = decode_img(image)
        if len(data) > 0:
            break
        data = extract_barcode(image)
        if len(data) == 1:
            break
        rate += 15
        video.set(1, rate)
        success, image = video.read()
    print(data)
    return 0


def live_detection():
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame by frame
        ret, frame = cap.read()

        data = decode_img(frame)
        if len(data) > 0:
            print(data)
            sleep(1)
        data = extract_barcode(frame)
        if len(data) > 0:
            print(data)
            sleep(1)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return 0


def main():
    args = parse_arguments()
    if args is None:
        exit(1)

    if args['image'] is not None:
        image = cv2.imread(args['image'])
        if image is None:
            print('Wrong path given or wrong format file')
            exit(1)
        data = decode_img(image)
    elif args['video'] is not None:
        decode_video(args)
    elif args['live'] is True:
        live_detection()
    return 0


if __name__ == '__main__':
    main()
