import cv2
import numpy as np
from matplotlib import pyplot as plt
img = np.zeros((512,512),np.uint8)
cv2.line(img,(0,0),(511,511),255,1)
cv2.imshow("grey",img)
cv2.waitKey()