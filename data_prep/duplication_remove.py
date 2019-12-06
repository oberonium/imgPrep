# -*- coding: utf-8 -*-
"""
# File Name : 
# Objective : 
# Created by:
# Created on: 2019/11/27
# Modified  : 2019/11/27
# Usage     :
# Input&Output:
"""
# for check duplication in training dataset

import argparse
import cv2
import numpy as np
import os
import time
from PIL import Image

# get parameters
def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", help = "source dataset dir")
    parser.add_argument("-t", "--target", help = "target dataset dir")
    parser.add_argument("-o", "--output", help = "output file")
    args = parser.parse_args()
    return args

# check two image difference
def check_duplication(input1, input2):
    img1 = cv2.imread(input1)
    img2 = cv2.imread(input2)
    difference = cv2.subtract(img1, img2)
    result = not np.any(difference)  # if difference is all zeros, False will be return
    if result is True:
        # print("fail check")
        print(input1, input2)
    else:
        pass
        # print("check")
    return


if __name__ == "__main__":
    start = time.time()
    # argument = get_argument()
    # imglist = os.listdir("/storage/dataprep_test/test_img/")
    # img=Image.open("/storage/dataprep_test/test_img/H_20.png")
    # print(len(img.split()))
    source="/storage/dataprep_test/test_img/"
    target="/storage/dataprep_test/test_img2/"
    img_source = os.listdir(source)
    img_target = os.listdir(target)

    # target dir img self check
    for i in img_target:
        for j in img_target:
            if i!=j:
                check_duplication(target+i, target+j)

    # target dir img check with source dir img
    for i in img_source:
        for j in img_target:
            check_duplication(source + i, target + j)

    end = time.time()
    print('[Finish time] Running time: %.0f min' % ((end - start) / 60))
