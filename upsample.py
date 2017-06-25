import numpy as np
import cv2 as cv
import os
from scipy.ndimage import zoom

inputpath = ".\\downsample"
outputpath = ".\\upsample"
sourcepath = ".\\inputImages"

wlist = []

for root,folders,files in os.walk(sourcepath):
    for file in files:
        image = cv.imread(root+"\\"+file)
        height, width, channels = image.shape
        wlist.append(width)


for root,folders,files in os.walk(inputpath):
    # loop the images
    for file in files:
        image = cv.imread(root+"\\"+file)

        height, width, channels = image.shape

        index = 0

        height = height*(wlist[index]/32)

        scaledImage = cv.resize(image,(wlist[index], int(height)),interpolation=cv.INTER_CUBIC)

        index += 1

        cv.namedWindow(file, cv.WINDOW_NORMAL)

        cv.imshow(file, image)

        # write out the new accessed images
        cv.imwrite(outputpath+"\\"+file,scaledImage)
        #cv.waitKey(0)
        cv.destroyAllWindows()