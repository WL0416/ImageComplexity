import numpy as np
import cv2 as cv
import os
from scipy.stats import entropy

inputpath = ".\\outputImages"

for root, folders, files in os.walk(inputpath):
    inputvalue = []

    # loop the images
    for file in files:
        index = 0
        image = cv.imread(root + "\\" + file)
        for i in image:
            rowvalue = []
            for j in i:
                rowvalue.append(j[0])
            inputvalue.append(rowvalue)
        print(len(inputvalue))

        for k in inputvalue:
            print(k)
        e = entropy(inputvalue)
        print(e)
        break
