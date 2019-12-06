# -*- coding: utf-8 -*-
"""
# File Name : 
# Objective : 
# Created by:
# Created on: 2019/12/3
# Modified  : 2019/12/3
# Usage     :
# Input&Output:
"""

# flip images and label xml file (PASCAL version)

import sys
import cv2
import time
import xml.etree.ElementTree as etree

# flip image: up/down, left/right, up/down+left/right
def flip(img):
    img_matrix=cv2.imread(img)
    img_flipup=cv2.flip(img_matrix, 0)
    img_fliplr=cv2.flip(img_matrix, 1)
    img_flip_uplr=cv2.flip(img_matrix, -1)
    cv2.imwrite(img[:-4]+"-up.png", img_flipup)
    cv2.imwrite(img[:-4]+"-lr.png", img_fliplr)
    cv2.imwrite(img[:-4]+"-uplr.png", img_flip_uplr)
    return

# flip xml file: up/down, left/right, up/down+left/right
def flip_label(labelXml):
    newXml_lr=labelXml[:-4]+"-lr.xml"
    newXml_up=labelXml[:-4]+"-up.xml"
    newXml_uplr=labelXml[:-4]+"-uplr.xml"

#left/right
    xmldata=etree.parse(labelXml)
    root = xmldata.getroot()
    width = int(root.find("size").find("width").text)
    filename = root.find("filename").text+"-lr"
    root.find("filename").text=str(filename)
    for object in root.iter("object"):
        xmin = width - int(object.find("bndbox").find("xmin").text)
        xmax = width - int(object.find("bndbox").find("xmax").text)
        object.find("bndbox").find("xmin").text=str(xmin)
        object.find("bndbox").find("xmax").text=str(xmax)
        xmldata.write(newXml_lr)

#up/down
    xmldata=etree.parse(labelXml)
    root = xmldata.getroot()
    height = int(root.find("size").find("height").text)
    filename = root.find("filename").text+"-up"
    root.find("filename").text=str(filename)
    for object in root.iter("object"):
        ymin = height - int(object.find("bndbox").find("ymin").text)
        ymax = height - int(object.find("bndbox").find("ymax").text)
        object.find("bndbox").find("ymin").text=str(ymin)
        object.find("bndbox").find("ymax").text=str(ymax)
        xmldata.write(newXml_up)

#left/right and up/down
    xmldata=etree.parse(labelXml)
    root = xmldata.getroot()
    width = int(root.find("size").find("width").text)
    height = int(root.find("size").find("height").text)
    filename = root.find("filename").text+"-uplr"
    root.find("filename").text=str(filename)
    for object in root.iter("object"):
        xmin = width - int(object.find("bndbox").find("xmin").text)
        xmax = width - int(object.find("bndbox").find("xmax").text)
        ymin = height - int(object.find("bndbox").find("ymin").text)
        ymax = height - int(object.find("bndbox").find("ymax").text)
        object.find("bndbox").find("xmin").text=str(xmin)
        object.find("bndbox").find("xmax").text=str(xmax)
        object.find("bndbox").find("ymin").text=str(ymin)
        object.find("bndbox").find("ymax").text=str(ymax)
        xmldata.write(newXml_uplr)

    return

if __name__=="__main__":
    start=time.time()
    flip("/storage/dataprep_test/test_img/H_20.png")
    flip_label("/storage/dataprep_test/Annotations/H_20.xml")
    end=time.time()
    print('[Finish time] Running time: %.0f min' % ((end - start) / 60))
