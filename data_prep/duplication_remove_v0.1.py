# -*- coding: utf-8 -*-
"""
# File Name : 
# Objective : 
# Created by:
# Created on: 2019/11/27
# Modified  : 2019/12/04
# Usage     :
# Input&Output:
"""
# for check duplication in training dataset

# new feature: using md5 instead of image matrix
import argparse
import cv2
import numpy as np
import os
import time
import hashlib

# get parameters
def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", help = "source dataset dir")
    parser.add_argument("-t", "--target", help = "target dataset dir")
    parser.add_argument("-o", "--output", help = "output file")
    args = parser.parse_args()
    return args

# generate md5 list for images
# check duplication
def md5_list_target(dir):
    #print(dir)
    md5list = {}
    img_dir = os.listdir(dir)
    for img in img_dir:
        image_file = open(dir + img, "rb").read()
        md5list[img] = hashlib.md5(image_file).hexdigest()

    reverse_dict = {}
    for key, value in md5list.items():
        try:
            reverse_dict[value].append(key)
        except:
            reverse_dict[value] = [key]

    a = [value for key, value in reverse_dict.items() if len(value) > 1]
    if len(a) == 0:
        print("[NOTICE] NO duplicate within dir")
    else:
        print("[NOTICE] duplication found!")
        print(a)

    return reverse_dict


# generate md5 for images
def md5_list(dir):
    #print(dir)
    md5list = {}
    img_dir = os.listdir(dir)
    for img in img_dir:
        image_file = open(dir + img, "rb").read()
        md5list[hashlib.md5(image_file).hexdigest()] = img
    return md5list

# dump function
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
    argument = get_argument()
    source = argument.source
    target = argument.target
    #source = "/storage/dataprep_test/test_img/"
    #target = "/storage/dataprep_test/test_img2/"
    img_source = os.listdir(source)
    img_target = os.listdir(target)
    target_dict = md5_list_target(target)
    source_dict = md5_list(source)

    # check dup image between target and source directory
    for key, _ in target_dict.items():
        if key in source_dict:
            print(target_dict[key], source_dict[key])

    end = time.time()
    print('[Finish time] Running time: %.0f min' % ((end - start) / 60))
