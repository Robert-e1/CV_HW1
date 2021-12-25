# relevant methods, functions used in Tic Tac Toe monitoring

# import relevant libraries
import cv2 as cv
import cv2.cv2
import numpy as np
import imutils
import math

# Function for detecting shapes (X or O)
# Function is based on Ramer-Douglas-Peucker algorithm
def detectShape( img, frameNumber, totalFrames ):
    # global variables
    monitor = np.zeros([800, 600, 3], dtype='uint8')
    cv.line(monitor, (200, 0), (200, 600), (0, 0, 255), 3)
    cv.line(monitor, (400, 0), (400, 600), (0, 0, 255), 3)
    cv.line(monitor, (0, 200), (600, 200), (0, 0, 255), 3)
    cv.line(monitor, (0, 400), (600, 400), (0, 0, 255), 3)
    winnerLineOffset = [-200, 0, 200]
    shape = "NA"                                                                            # initialize the shape as NA - not available
    gameStatus = 0          # initialize tie
    TopLeftPoint = [0, 0]   # initialize intersections of grid
    TopRightPoint = [0, 0]
    BotLeftPoint = [0, 0]
    BotRightPoint = [0, 0]

    progress = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]    # initialize game progress
                                                    # 0 -> field blank atm
                                                    # -1 -> 'X'
                                                    # 1  -> 'O'
    #cv.imshow('Orig', img)                                                                  # show original frame
    # convert image to grayscale and add slight blur:
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred_img = cv.GaussianBlur(gray_img, (3, 3), 3)
    #eroded = cv.erode(blurred_img, (3,3), iterations=2)
    #dilate = cv.dilate(eroded, (3,5), iterations=2)
    #blurred_img = cv.GaussianBlur(eroded, (3, 3), 1)

    # threshold image to create a binary image
    thresh_img = cv.threshold(blurred_img, 165, 255, cv.THRESH_BINARY)[1]

    cv.imshow('Thresholded video', thresh_img)

    contour_list = cv.findContours(thresh_img.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_NONE)   # find contours of thresholded image
    contour_list = imutils.grab_contours(contour_list)                                      # <- store contours in list/sequence
    print(len(contour_list))

#******************************************************************************************************************************************************#
    for c in range(len(contour_list)):                                      # find edge points of center rectangle
        perimiter = cv.arcLength(contour_list[c], True)                     # calculate te perimiter of the detected object/shape
        approx = cv.approxPolyDP(contour_list[c], 0.04 * perimiter, True)   # built-in function for approximating the detected contour ->

        M = cv.moments(approx)                     # find countour centres using geometric moments
        if (M["m00"] != 0):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if ((len(approx) == 4)):                            # possibly detected center field of grid    -> use this for calculating rectangle edges
                if(abs(approx[0][0][0]-approx[3][0][0]) < 100 and abs(approx[0][0][0]-approx[3][0][0]) > 20):       # center field of grid detected
                    print("here")
                    TopLeftPoint = approx[0][0]
                    BotLeftPoint= approx[1][0]
                    BotRightPoint = approx[2][0]
                    TopRightPoint = approx[3][0]
# ******************************************************************************************************************************************************#

# ******************************************************************************************************************************************************#
    for c in range(len(contour_list)):
        perimiter = cv.arcLength(contour_list[c], True)                     # calculate te perimiter of the detected object/shape
        approx = cv.approxPolyDP(contour_list[c], 0.04 * perimiter, True)   # built-in function for approximating the detected contour ->

        M = cv.moments(approx)                     # find countour centres using geometric moments
        if (M["m00"] != 0):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            print("Value of approx is: " + str(len(approx)))    # this line is used for testing

            if ((len(approx) < 4) or (len(approx) > 9)):        # rectangle or border detected -> skip
                continue
            elif ((len(approx) == 4)):                            # possibly detected center field of grid    -> use this for calculating game progress
                if(abs(approx[0][0][0]-approx[3][0][0]) < 100 and abs(approx[0][0][0]-approx[3][0][0]) > 20):       # center field of grid detected
                    print("here")
                    TopLeftPoint = approx[0][0]
                    BotLeftPoint= approx[1][0]
                    BotRightPoint = approx[2][0]
                    TopRightPoint = approx[3][0]

                    if (approx[0][0][0] <= approx[1][0][0]):                     # -> grid rotation angle < 0
                        line1_deltax_vertical = abs(approx[0][0][0] - approx[1][0][0])
                        line1_deltay_vertical = abs(approx[0][0][1] - approx[1][0][1])
                        line2_deltax_vertical = abs(approx[3][0][0] - approx[2][0][0])
                        line2_deltay_vertical = abs(approx[3][0][1] - approx[2][0][1])
                        line1_deltax_horizontal = abs(approx[0][0][0] - approx[3][0][0])
                        line1_deltay_horizontal = abs(approx[0][0][1] - approx[3][0][1])
                        line2_deltax_horizontal = abs(approx[1][0][0] - approx[2][0][0])
                        line2_deltay_horizontal = abs(approx[1][0][1] - approx[2][0][1])
                    else:                                                                           # -> grid rotation angle > 0
                        line1_deltax_vertical = -abs(approx[0][0][0] - approx[1][0][0])
                        line1_deltay_vertical = abs(approx[0][0][1] - approx[1][0][1])
                        line2_deltax_vertical = -abs(approx[3][0][0] - approx[2][0][0])
                        line2_deltay_vertical = abs(approx[3][0][1] - approx[2][0][1])
                        line1_deltax_horizontal = abs(approx[0][0][0] - approx[3][0][0])
                        line1_deltay_horizontal = -abs(approx[0][0][1] - approx[3][0][1])
                        line2_deltax_horizontal = abs(approx[1][0][0] - approx[2][0][0])
                        line2_deltay_horizontal = -abs(approx[1][0][1] - approx[2][0][1])

                    cv.line(img, (approx[0][0][0]-line1_deltax_horizontal, approx[0][0][1])-line1_deltay_horizontal, (approx[3][0][0]+line1_deltax_horizontal, approx[3][0][1]+line1_deltay_horizontal), (0, 0, 255), 3)    # upper horizontal line
                    cv.line(img, (approx[0][0][0]+line1_deltax_vertical, approx[0][0][1]-line1_deltay_vertical), (approx[1][0][0]-line1_deltax_vertical, approx[1][0][1]+line1_deltay_vertical), (0, 0, 255), 3)            # left vertical line
                    cv.line(img, (approx[1][0][0]-line2_deltax_horizontal, approx[1][0][1]-line2_deltay_horizontal), (approx[2][0][0]+line2_deltax_horizontal, approx[2][0][1]+line2_deltay_horizontal), (0, 0, 255), 3)    # bottom horizontal line
                    cv.line(img, (approx[2][0][0]-line2_deltax_vertical, approx[2][0][1]+line2_deltay_vertical), (approx[3][0][0]+line2_deltax_vertical, approx[3][0][1]-line2_deltay_vertical), (0, 0, 255), 3)            # right vertical line
                    continue

            elif ((len(approx) >= 5) and (len(approx) <= 7)):   # circle detected
                shape = "O"
                print("O detected")

                cv.drawContours(img, contour_list[c], -1, (0, 255, 0), 2)  # draw contours
                cv.putText(img, shape, (cX, cY-5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                if ((abs(cX - BotRightPoint[0]) < 200) and (abs(cY - BotRightPoint[1]) < 200)):
                    progress = gameProgress(cX, cY, shape, TopLeftPoint, TopRightPoint, BotLeftPoint, BotRightPoint, progress )
                    monitorProgress(monitor, progress)
                    gameStatus, Combination = winnerFound(progress)


            else:                                               # anything else is X -> assuming players are only allowed to put 'X' or 'O'
                shape = "X"
                print("X detected")

                cv.drawContours(img, contour_list[c], -1, (0, 255, 0), 2)  # draw contours
                cv.putText(img, shape, (cX, cY-5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                if ((abs(cX - BotRightPoint[0]) < 200) and (abs(cY - BotRightPoint[1]) < 200)):
                    progress = gameProgress(cX, cY, shape, TopLeftPoint, TopRightPoint, BotLeftPoint, BotRightPoint, progress )
                    monitorProgress(monitor, progress)
                    gameStatus, Combination = winnerFound(progress)

    # PRINT WINNER ON MONITOR
    if (frameNumber == totalFrames):
        if (gameStatus == -1):
            print("X won !")
            if ((Combination < 4) and (Combination > 0)):
                cv.line(monitor, (20, 300+winnerLineOffset[Combination-1]), (580, 300+winnerLineOffset[Combination-1]), (0, 255, 0), 3)
            elif((Combination >=4) and (Combination <7) ):
                cv.line(monitor, (300+winnerLineOffset[Combination-1], 20 ), (300+winnerLineOffset[Combination-1], 580), (0, 255, 0), 3)

            cv.putText(monitor, "'X' WON !", (10, 740), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), )
        elif (gameStatus == 1):
            print("O won !")
            if ((Combination < 4) and (Combination > 0)):
                cv.line(monitor, (20, 300+winnerLineOffset[Combination-1]), (580, 300+winnerLineOffset[Combination-1]), (0, 255, 0), 3)
            elif((Combination >=4) and (Combination <7) ):
                cv.line(monitor, (300+winnerLineOffset[Combination-1], 20 ), (300+winnerLineOffset[Combination-1], 580), (0, 255, 0), 3)

            cv.putText(monitor, "'O' WON !", (10, 740), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 2)

        else:
            cv.putText(monitor, "TIE !", (160, 740), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 2)
            print("Game ended in tie ! !")
    else:
        print("Game Still in progress !")

    cv.imshow('Monitor for game progress', monitor)

#******************************************************************************************************************************************************#
########################################################################################################################################################

# Function for keeping track of game progress
def gameProgress(cX, cY, shape, TopLeftPoint, TopRightPoint, BotLeftPoint, BotRightPoint, progress):
    if (cX < min(TopLeftPoint[0],BotLeftPoint[0])):          # shape is in left column of the grid
        if (cY < min(TopLeftPoint[1], TopRightPoint[1])):       # shape is in top row
            if (shape == "O"):
                progress[0][0] = 1
            else:
                progress[0][0] = -1
        elif(cY > max(BotLeftPoint[1], BotRightPoint[1])):      # shape is in bottom row
            if (shape == "O"):
                progress[2][0] = 1
            else:
                progress[2][0] = -1
        else:                                                   # shape is in middle row
            if (shape == "O"):
                progress[1][0] = 1
            else:
                progress[1][0] = -1
    elif(cX > max(TopRightPoint[0], BotRightPoint[0])):      # shape is in right column of the grid
        if (cY < min(TopLeftPoint[1], TopRightPoint[1])):       # shape is in top row
            if (shape == "O"):
                progress[0][2] = 1
            else:
                progress[0][2] = -1
        elif(cY > max(BotLeftPoint[1], BotRightPoint[1])):      # shape is in bottom row
            if (shape == "O"):
                progress[2][2] = 1
            else:
                progress[2][2] = -1
        else:                                                   # shape is in middle row
            if (shape == "O"):
                progress[1][2] = 1
            else:
                progress[1][2] = -1
    else:                                                    # shape is in middle column of the grid
        if (cY < min(TopLeftPoint[1], TopRightPoint[1])):       # shape is in top row
            if (shape == "O"):
                progress[0][1] = 1
            else:
                progress[0][1] = -1
        elif(cY > max(BotLeftPoint[1], BotRightPoint[1])):      # shape is in bottom row
            if (shape == "O"):
                progress[2][1] = 1
            else:
                progress[2][1] = -1
        else:                                                   # shape is in middle row
            if (shape == "O"):
                progress[1][1] = 1
            else:
                progress[1][1] = -1

    #print(cX, cY)
    #print(TopLeftPoint)
    #print(BotLeftPoint)
    #print(BotRightPoint)
    #print(TopRightPoint)
    #print("Progress is: \n")
    print(progress)
    return progress
        # Function for detecting grid
########################################################################################################################################################

# Function for determining if a player has won
# Return values:
#   -1 -> X won
#    1 -> O won
#    0 -> game in progress/tie
def winnerFound(progress):
    if (sum(progress[0]) == -3):            # Checking horizontal vectors for winner
        return [-1,1]
    elif(sum(progress[1]) == -3):           # Checking horizontal vectors for winner
        return [-1,2]
    elif(sum(progress[2]) == -3):           # Checking horizontal vectors for winner
        return [-1,3]
    elif (sum(progress[0]) == 3):
        return [1,1]
    elif (sum(progress[1]) == 3):
        return [1,2]
    elif (sum(progress[2]) == 3):
        return [1,3]
    elif ((progress[0][0] + progress[1][0] + progress[2][0]) == -3):    # Checking vertical vectors for winner
        return [-1,4]
    elif ((progress[0][1] + progress[1][1] + progress[2][1]) == -3):    # Checking vertical vectors for winner
        return [-1,5]
    elif ((progress[0][2] + progress[1][2] + progress[2][2]) == -3):    # Checking vertical vectors for winner
        return [-1,6]
    elif ((progress[0][0] + progress[1][0] + progress[2][0]) == 3):
        return [1,4]
    elif ((progress[0][1] + progress[1][1] + progress[2][1]) == 3):
        return [1,5]
    elif ((progress[0][2] + progress[1][2] + progress[2][2]) == 3):
        return [1,6]
    elif ((progress[0][0] + progress[1][1] + progress[2][2]) == -3):
        return [-1,7]
    elif ((progress[0][2] + progress[1][1] + progress[2][0]) == -3):    #Check diagonal vector for winner
        return [-1,7]
    elif ((progress[0][0] + progress[1][1] + progress[2][2]) == 3):
        return [1,8]
    elif ((progress[0][2] + progress[1][1] + progress[2][0]) == 3):
        return [1,8]
    else:
        return [0,0]

########################################################################################################################################################

def drawShape(img, shape, offset):
    if (shape == "X"):
        cv.line(img, (220+offset[0], 220+offset[1]), (380+offset[0], 380+offset[1]), (0, 255, 0), 3)
        cv.line(img, (220+offset[0], 380+offset[1]), (380+offset[0], 220+offset[1]), (0, 255, 0), 3)
    else:
        cv.circle(img, (300+offset[0], 300+offset[1]), 80, (0, 255, 0), 3)

########################################################################################################################################################
def monitorProgress(img, progress):
    offset = [[[-200, -200], [0, -200], [200, -200]], [[-200, 0], [0, 0], [200, 0]],
              [[-200, 200], [0, 200], [200, 200]]]

    for i in range(3):                                          # loop through matrix representing game progress
        for j in range(3):
            if (progress[i][j] == -1):
                drawShape(img, "X", offset[i][j])
            elif (progress[i][j] == 1):
                drawShape(img, "O", offset[i][j])

########################################################################################################################################################

########################################################################################################################################################

# Function is based on HoughLines
def detectGrid( img ):
    edges = cv.Canny( img, 200, 200, None, 3 )                                                      # extract edges of frame
    edges_blurred = cv.GaussianBlur(edges, (5, 5), 2)                                               # add blur
    lines = cv.HoughLinesP( edges_blurred, 1, np.pi / 180, 150, minLineLength=100, maxLineGap=10 )   # detect lines using probabilistic method
    print("Number of detected lines: " + str(len(lines)))
    cv.imshow('Detected edges', edges_blurred)

    for line in lines:
        x1,y1,x2,y2 = line[0]

        cv.line(img, (x1,y1), (x2,y2), (0,0,255), 2)                                            # draw first line


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
