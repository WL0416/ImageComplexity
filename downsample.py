import numpy as np
import cv2 as cv
import os
from scipy.ndimage import zoom

inputpath = ".\\inputImages"
outputpath = ".\\downsample"

for root,folders,files in os.walk(inputpath):
    # loop the images
    for file in files:
        image = cv.imread(root+"\\"+file)

        height, width, channels = image.shape

        height = height / (width / 32)

        scaledImage = cv.resize(image,(32, int(height)),interpolation=cv.INTER_CUBIC)

        cv.namedWindow(file, cv.WINDOW_NORMAL)

        cv.imshow(file, image)

        # write out the new accessed images
        cv.imwrite(outputpath+"\\"+file,scaledImage)
        #cv.waitKey(0)
        cv.destroyAllWindows()