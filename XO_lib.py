# relevant methods, functions used in Tic Tac Toe monitoring

# import relevant libraries
import cv2 as cv
import imutils

# function for detecting shapes (X or O)
# function is based on Ramer-Douglas-Peucker algorithm
def detectShape( img ):
    shape = "NA"                                                                            # initialize the shape as NA - not available
    skip_flag = False

    cv.imshow('Orig', img)                                                                  # show original frame
    # convert image to grayscale and add slight blur:
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred_img = cv.GaussianBlur(gray_img, (3, 3), 0)

    # threshold image to create a binary image
    thresh_img = cv.threshold(blurred_img, 170, 255, cv.THRESH_BINARY)[1]
    cv.imshow('thresholded', thresh_img)

    contour_list = cv.findContours(thresh_img.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_NONE)   # find contours of thresholded image
    contour_list = imutils.grab_contours(contour_list)                                      # <- store contours in list/sequence
    print(len(contour_list))

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

        if ((len(approx) <= 4) or (len(approx) > 10)):                            # rectangle or border detected -> skip
            continue
        elif ((len(approx) >= 5) and (len(approx) <= 7)):   # circle detected
            shape = "O"
            if (skip_flag):
                skip_flag = False
                continue                                    # for circles ('O') both inner and outer edges are detected -> skip one
            skip_flag = True
        else:                                               # anything else is X -> assuming players are only allowed to put 'X' or 'O'
            shape = "X"

        cv.drawContours(img, contour_list[c], -1, (0, 255, 0), 2)                           # draw contours
        cv.putText(img, shape, (cX, cY), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv.imshow("test_img", img)




