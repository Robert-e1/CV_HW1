# relevant methods, functions used in Tic Tac Toe monitoring

# import relevant libraries
import cv2 as cv
import cv2.cv2
import numpy as np
import imutils
import math

# Function for detecting shapes (X or O)
# Function is based on Ramer-Douglas-Peucker algorithm
def detectShape( img ):
    shape = "NA"                                                                            # initialize the shape as NA - not available

    #cv.imshow('Orig', img)                                                                  # show original frame
    # convert image to grayscale and add slight blur:
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred_img = cv.GaussianBlur(gray_img, (3, 3), 0)

    # threshold image to create a binary image
    thresh_img = cv.threshold(blurred_img, 170, 255, cv.THRESH_BINARY)[1]
    cv.imshow('Thresholded video', thresh_img)

    contour_list, hier = cv.findContours(thresh_img.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_NONE)   # find contours of thresholded image
    #contour_list = imutils.grab_contours(contour_list)                                      # <- store contours in list/sequence
    print(len(contour_list))
    #print(hier)
    for c in range(len(contour_list)):
        perimiter = cv.arcLength(contour_list[c], True)                     # calculate te perimiter of the detected object/shape
        approx = cv.approxPolyDP(contour_list[c], 0.04 * perimiter, True)   # built-in function for approximating the detected contour ->


        M = cv.moments(contour_list[c])                     # find countour centres using geometric moments
        try:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        except:
            continue

        print("Value of approx is: " + str(len(approx)))    # this line is used for testing

        if ((len(approx) <= 4) or (len(approx) > 9)):       # rectangle or border detected -> skip
            continue
        elif ((len(approx) >= 5) and (len(approx) <= 7)):   # circle detected
            shape = "O"
        else:                                               # anything else is X -> assuming players are only allowed to put 'X' or 'O'
            shape = "X"

        cv.drawContours(img, contour_list[c], -1, (0, 255, 0), 2)                                   # draw contours
        cv.putText(img, shape, (cX, cY), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# Function for detecting grid
# Function is based on HoughLines
def detectGrid( img ):
    edges = cv.Canny( img, 200, 200, None, 3 )                                                      # extract edges of frame
    edges_blurred = cv.GaussianBlur(edges, (3, 3), 1)                                               # add blur
    lines = cv.HoughLinesP( edges_blurred, 1, np.pi / 180, 150, minLineLength=100, maxLineGap=10 )   # detect lines using probabilistic method
    print(len(lines))
    cv.imshow('Detected edges', edges_blurred)

    for line in lines:
        x1,y1,x2,y2 = line[0]

        cv.line(img, (x1,y1), (x2,y2), (0,0,255), 2)

# Function for detecting player's hand in image
# Based on total number of 0-value pixels
def frameIsStatic( curr_img ): #, prev_img ):
    curr_img_gray = cv.cvtColor(curr_img, cv.COLOR_BGR2GRAY)                                       # using delta of 2 subsequent frames not too reliable
    #prev_img_gray = cv.cvtColor(prev_img, cv.COLOR_BGR2GRAY)
    curr_img_bin = cv.threshold(curr_img_gray, 150, 255, cv2.cv2.THRESH_BINARY)[1]
    #prev_img_bin = cv.threshold(prev_img_gray, 100, 255, cv2.cv2.THRESH_BINARY)[1]
    #cv.imshow('a', curr_img_bin)
    #cv.imshow('b', prev_img_bin)

    #img_delta = cv.absdiff(curr_img_bin, prev_img_bin)
    #sum = np.sum(curr_img_bin == 0)
    sum = np.sum(curr_img_bin == 0)
    cv.imshow('Current image binarized', curr_img_bin)
    if ((sum > 6000)):
        return False
    else:

        return True
