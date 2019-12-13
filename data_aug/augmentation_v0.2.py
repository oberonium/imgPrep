# -*- coding: utf-8 -*-
"""
# File Name : 
# Objective : 
# Created by:
# Created on: 2019/12/6
# Modified  : 2019/12/13
# Usage     :
# Input&Output:
"""

# flip images and label xml file (PASCAL version)
# rotate images and object coordinates

# new feature: parameters

import os
import sys
import cv2
import time
import argparse
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as etree

# get parameters
def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--imagedir", help="image dir")
    parser.add_argument("-a", "--annotationdir", help="annotation xml file dir")
    parser.add_argument("-s", "--size", help="small, med, large (bounding box)")
    args = parser.parse_args()
    return args

# flip image: up/down, left/right, up/down+left/right
def flip(img):
    img_matrix = cv2.imread(img)
    img_flipup = cv2.flip(img_matrix, 0)
    img_fliplr = cv2.flip(img_matrix, 1)
    img_flip_uplr = cv2.flip(img_matrix, -1)
    cv2.imwrite(img[:-4] + "-up.png", img_flipup)
    cv2.imwrite(img[:-4] + "-lr.png", img_fliplr)
    cv2.imwrite(img[:-4] + "-uplr.png", img_flip_uplr)
    return


# flip xml file: up/down, left/right, up/down+left/right
def flip_label(labelXml):
    newXml_lr = labelXml[:-4] + "-lr.xml"
    newXml_up = labelXml[:-4] + "-up.xml"
    newXml_uplr = labelXml[:-4] + "-uplr.xml"

    # left/right
    xmldata = etree.parse(labelXml)
    root = xmldata.getroot()
    width = int(root.find("size").find("width").text)
    filename = root.find("filename").text + "-lr"
    root.find("filename").text = str(filename)
    for object in root.iter("object"):
        xmin = width - int(object.find("bndbox").find("xmin").text)
        xmax = width - int(object.find("bndbox").find("xmax").text)
        object.find("bndbox").find("xmin").text = str(xmin)
        object.find("bndbox").find("xmax").text = str(xmax)
        xmldata.write(newXml_lr)

    # up/down
    xmldata = etree.parse(labelXml)
    root = xmldata.getroot()
    height = int(root.find("size").find("height").text)
    filename = root.find("filename").text + "-up"
    root.find("filename").text = str(filename)
    for object in root.iter("object"):
        ymin = height - int(object.find("bndbox").find("ymin").text)
        ymax = height - int(object.find("bndbox").find("ymax").text)
        object.find("bndbox").find("ymin").text = str(ymin)
        object.find("bndbox").find("ymax").text = str(ymax)
        xmldata.write(newXml_up)

    # left/right and up/down
    xmldata = etree.parse(labelXml)
    root = xmldata.getroot()
    width = int(root.find("size").find("width").text)
    height = int(root.find("size").find("height").text)
    filename = root.find("filename").text + "-uplr"
    root.find("filename").text = str(filename)
    for object in root.iter("object"):
        xmin = width - int(object.find("bndbox").find("xmin").text)
        xmax = width - int(object.find("bndbox").find("xmax").text)
        ymin = height - int(object.find("bndbox").find("ymin").text)
        ymax = height - int(object.find("bndbox").find("ymax").text)
        object.find("bndbox").find("xmin").text = str(xmin)
        object.find("bndbox").find("xmax").text = str(xmax)
        object.find("bndbox").find("ymin").text = str(ymin)
        object.find("bndbox").find("ymax").text = str(ymax)
        xmldata.write(newXml_uplr)

    return


# rotate img with certain angle.
def rotation(img, angle, scale):
    img_matrix = cv2.imread(img)
    #    hist = cv2.calcHist(img_matrix, [0], None, [256], [0, 256])
    #    print(hist)
    #    plt.hist(img_matrix.ravel(), 256, [0,256])
    #    plt.show()
    #print(img_matrix.shape)
    rows, cols = img_matrix.shape[:2]
    rotate_matrix = cv2.getRotationMatrix2D((cols / 2.0, rows / 2.0), angle, scale)
    #print(rotate_matrix)
    img_matrix_new = cv2.warpAffine(img_matrix, rotate_matrix, (cols, rows))
    #print(img_matrix_new.shape)
    cv2.imwrite(img[:-4] + "-rotate_"+str(angle)+".png", img_matrix_new)

    return


def rotate_label(labelXml, angle, scale, size):
    newXml_rot = labelXml[:-4] + "-rotate_"+str(angle)+".xml"
    xmldata = etree.parse(labelXml)
    root = xmldata.getroot()
    width = int(root.find("size").find("width").text)
    height = int(root.find("size").find("height").text)

    re_angle = np.deg2rad(angle)
    new_width = width
    new_height = height
    # new_width = (abs(np.sin(re_angle) * height) + abs(np.cos(re_angle) * width)) * scale
    # new_height = (abs(np.cos(re_angle) * height) + abs(np.sin(re_angle) * width)) * scale

    #print(new_width, new_height)
    rotate_matrix = cv2.getRotationMatrix2D((new_width * 0.5, new_height * 0.5), angle, scale)
    rotate_move = np.dot(rotate_matrix, np.array([(new_width - width) * 0.5, (new_height - height) * 0.5, 0]))
    rotate_matrix[0, 2] += rotate_move[0]
    rotate_matrix[1, 2] += rotate_move[1]

    # get original anchor coordinate, rotate.
    # for object in root.iter("object"):
    for object in root.findall("object"):
        xmin = int(object.find("bndbox").find("xmin").text)
        xmax = int(object.find("bndbox").find("xmax").text)
        ymin = int(object.find("bndbox").find("ymin").text)
        ymax = int(object.find("bndbox").find("ymax").text)

        point1 = np.dot(rotate_matrix, np.array([xmin, ymin, 1]))  # large one
        point2 = np.dot(rotate_matrix, np.array([xmax, ymin, 1]))
        point3 = np.dot(rotate_matrix, np.array([xmax, ymax, 1]))
        point4 = np.dot(rotate_matrix, np.array([xmin, ymax, 1]))

        point1_1 = np.dot(rotate_matrix, np.array([(xmin + xmax) / 2, ymin, 1]))  # small one
        point2_1 = np.dot(rotate_matrix, np.array([xmax, (ymin + ymax) / 2, 1]))
        point3_1 = np.dot(rotate_matrix, np.array([(xmin + xmax) / 2, ymax, 1]))
        point4_1 = np.dot(rotate_matrix, np.array([xmin, (ymin + ymax) / 2, 1]))

        if size == "small":
            point1 = point1_1
            point2 = point2_1
            point3 = point3_1
            point4 = point4_1
        elif size == "med":
            point1 = (point1 + point1_1) / 2
            point2 = (point2 + point2_1) / 2
            point3 = (point3 + point3_1) / 2
            point4 = (point4 + point4_1) / 2
        elif size == "large":
            pass

        concat = np.vstack((point1, point2, point3, point4))  # to np.array

        concat = concat.astype(np.int32)
        rx, ry, rw, rh = cv2.boundingRect(concat)
        new_xmin = rx
        new_ymin = ry
        new_xmax = rx + rw
        new_ymax = ry + rh
        object.find("bndbox").find("xmin").text = str(new_xmin)
        object.find("bndbox").find("xmax").text = str(new_xmax)
        object.find("bndbox").find("ymin").text = str(new_ymin)
        object.find("bndbox").find("ymax").text = str(new_ymax)

        # remove out-of-range(img) b-box
        if new_ymax<0 or new_ymin<0 or new_xmin<0 or new_xmax<0 or new_xmax>width or new_xmin>width or new_ymin>height or new_ymax>height:
            root.remove(object)
        else:
            xmldata.write(newXml_rot)

    #print(newXml_rot)

    return


if __name__ == "__main__":
    start = time.time()

    argument =get_argument()
    imglist_dir=os.listdir(argument.imagedir)
    img_dir=argument.imagedir
    xml_dir=argument.annotationdir

    # flip left/right
    for img in imglist_dir:
        if os.path.exists(xml_dir+img[:-4]+".xml"):
            flip(img_dir+img)
            flip_label(xml_dir+img[:-4]+".xml")

    # rotation
    for img in imglist_dir:
        for angle in range(1,180):
            if os.path.exists(xml_dir+img[:-4]+".xml"):
                rotation(img_dir+img, angle, 1)
                rotate_label(xml_dir+img[:-4]+".xml", angle, 1, "med")
            else:
                pass

    end = time.time()
    print('[Finish time] Running time: %.0f min' % ((end - start) / 60))
