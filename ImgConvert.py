"""
Author: Wei Li
Image Generation Script
"""
import numpy as np
import cv2 as cv
import os

inputpath = ".\\inputImages"
outputpath = ".\\outputImages"


def blur(inputpath):
    # loop the target folder to get the original images' information
    for root, folders, files in os.walk(inputpath):
        # loop the images
        for file in files:
            image = cv.imread(root + "\\" + file)

            blurImage = cv.GaussianBlur(image, (5, 5), 0)

            cv.namedWindow(file, cv.WINDOW_NORMAL)
            cv.imshow(file, image)

            # write out the new accessed images
            cv.imwrite(outputpath + "\\" + file, blurImage)
            # cv.waitKey(0)
            cv.destroyAllWindows()

def downsample(outputpath):
    for root, folders, files in os.walk(outputpath):
        # loop the images
        for file in files:
            image = cv.imread(root + "\\" + file)

            height, width, channels = image.shape

            height = height / (width / 32)

            scaledImage = cv.resize(image, (32, int(height)), interpolation=cv.INTER_CUBIC)

            cv.namedWindow(file, cv.WINDOW_NORMAL)

            cv.imshow(file, image)

            # write out the new accessed images
            cv.imwrite(outputpath + "\\" + file, scaledImage)
            # cv.waitKey(0)
            cv.destroyAllWindows()

def upsample(inputpath, ouputpath):

    wlist = []

    for root, folders, files in os.walk(inputpath):
        for file in files:
            image = cv.imread(root + "\\" + file)
            height, width, channels = image.shape
            wlist.append(width)

    for root, folders, files in os.walk(outputpath):
        # loop the images
        for file in files:
            image = cv.imread(root + "\\" + file)

            height, width, channels = image.shape

            index = 0

            height = height * (wlist[index] / 32)

            scaledImage = cv.resize(image, (wlist[index], int(height)), interpolation=cv.INTER_CUBIC)

            index += 1

            cv.namedWindow(file, cv.WINDOW_NORMAL)

            cv.imshow(file, image)

            # write out the new accessed images
            cv.imwrite(outputpath + "\\" + file, scaledImage)
            # cv.waitKey(0)
            cv.destroyAllWindows()

def grayscale(outputpath):
    # loop the target folder to get the original images' information
    for root, folders, files in os.walk(outputpath):
        # loop the images
        for file in files:
            image = cv.imread(root + "\\" + file)
            # convert image's color into 8-bit gray
            grayImage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

            cv.namedWindow(file, cv.WINDOW_NORMAL)
            cv.imshow(file, image)

            # write out the new accessed images
            cv.imwrite(outputpath + "\\" + file, grayImage)
            # cv.waitKey(0)
            cv.destroyAllWindows()

blur(inputpath)
downsample(outputpath)
upsample(inputpath,outputpath)
grayscale(outputpath)