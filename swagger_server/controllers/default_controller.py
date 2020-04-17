import subprocess
import sys
import tempfile
import traceback

import cv2
import numpy as np
import os

import connexion
import urllib.request
from swagger_server.models.check_body import CheckBody  # noqa: E501
from swagger_server.models.check_response import CheckResponse  # noqa: E501


image_transforms = []
for filename in os.listdir("test_images"):
    img = cv2.imread("test_images/" + filename)
    sift = cv2.xfeatures2d.SIFT_create()
    image_transforms.append(sift.detectAndCompute(img, None))


def check_image_post(body):  # noqa: E501
    """check_image_post

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: CheckResponse
    """
    if connexion.request.is_json:
        body = CheckBody.from_dict(connexion.request.get_json())  # noqa: E501
    resp = urllib.request.urlopen(body.image_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return CheckResponse(accepted_num=__run_swift(image))


def __run_swift(input_img):
    MIN_MATCH_COUNT = 10

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    kp2, des2 = sift.detectAndCompute(input_img,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 100)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    match_count = 0
    for kp1, des1 in image_transforms:
        matches = flann.knnMatch(des1, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m,n in matches:
            if m.distance < 0.75*n.distance:
                good.append(m)

        if len(good)>MIN_MATCH_COUNT:
            match_count = match_count + 1
    return match_count


if __name__ == "__main__":
    resp = urllib.request.urlopen("https://i.ibb.co/dcLdwkS/kep2.jpg")
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    print(__run_swift(image))
