#coding: utf-8
import glob

import numpy as np
import cv2


CONTOUR_MIN_AREA = 250#50 #pixels squared
CONTOUR_MAX_AREA = 950#300

training_images = glob.glob('./training_images/*.jpg')
samples = np.empty((0, 100))
responses = []
keys = [i for i in range(49, 57)]

for image_path in training_images:

    im = cv2.imread(image_path)

    if "unwarp" in image_path:
        im = cv2.cvtColor(im, cv2.COLOR_HSV2RGB)

    bgr = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)

    gray = cv2.GaussianBlur(bgr, (5, 5), 0.5)
    gray = cv2.GaussianBlur(gray, (5, 5), 0.5)
    gray = cv2.GaussianBlur(gray, (9, 9), 0)

    corner_gray = cv2.inRange(gray, np.array([0, 0, 0], np.uint8), np.array([100, 120, 120], np.uint8))

    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, 0, 1, 5, 2)
    corner_thresh = cv2.adaptiveThreshold(corner_gray, 255, 0, 1, 5, 3)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    dilate = cv2.dilate(corner_thresh, kernel, iterations=0)
    erode = cv2.erode(dilate, kernel, iterations=0)
    dilate = cv2.dilate(erode, kernel, iterations=2)
    contours, hierarchy = cv2.findContours(dilate.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)



    #    for contour in contours:
    #        [x, y, w, h] = cv2.boundingRect(contour)
    #        area = h * w
    #        if CONTOUR_MIN_AREA < area < CONTOUR_MAX_AREA:
    #            ratio = h / w
    #            cv2.rectangle(thresh, (x, y), (x + w, y + h), (255, 255, 255), 2)
    #            print area, ratio
    #
    #    cv2.imshow("contours", thresh)
    #    cv2.waitKey()

    for contour in contours:
        [x, y, w, h] = cv2.boundingRect(contour)
        area = w * h
        if CONTOUR_MIN_AREA < area < CONTOUR_MAX_AREA:
            tolerance = 0
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
            roi = thresh[y - tolerance:y + h + tolerance, x - tolerance:x + w + tolerance]
            roismall = cv2.resize(roi, (10, 10))
            cv2.imshow('norm', im)
            key = cv2.waitKey(0)

            if key in keys:
                responses.append(int(chr(key)))
                sample = roismall.reshape((1, 100))
                samples = np.append(samples, sample, 0)

responses = np.array(responses, np.float32)
responses = responses.reshape((responses.size, 1))
np.savetxt('trained_data/generalsamples.data', samples)
np.savetxt('trained_data/generalresponses.data', responses)