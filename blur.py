import numpy as np
import cv2 as cv
import os

inputpath = ".\\inputImages"
outputpath = ".\\blur"

# loop the target folder to get the original images' information
for root, folders, files in os.walk(inputpath):
    # loop the images
    for file in files:
        image = cv.imread(root+"\\"+file)

        blurImage = cv.GaussianBlur(image,(10,10),0)

        cv.namedWindow(file, cv.WINDOW_NORMAL)
        cv.imshow(file, image)

        # write out the new accessed images
        cv.imwrite(outputpath+"\\"+file, blurImage)
        #cv.waitKey(0)
        cv.destroyAllWindows()