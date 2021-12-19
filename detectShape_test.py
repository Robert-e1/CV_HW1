import cv2.cv2

import XO_lib as XO
import cv2 as cv
import imutils

shape = ""

img = cv.imread('samples/test_img2.png')

shape = XO.detectShape(img)                           # execute shape detection

cv.waitKey(0)