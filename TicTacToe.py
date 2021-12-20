# Application/script for monitoring a match of tic-tac-toe.

# import relevant libraries
import sys
import cv2 as cv
import imutils
from imutils.video import count_frames

import XO_lib as XO

# global attributes:
import cv2.cv2
frame_counter = 0
videos = ["samples/xo1c.avi", "samples/xo1c.avi"]

# let user choose one of the available videos:
for s in range(len(videos)):
    print("To select " + videos[s] + ", press   " + str(s) + ".")
#video_idx = int(input())
video_idx = 1

if (video_idx < 1) or (video_idx > len(videos)):
    print("Wrong input selected -> terminating.")
    quit()
else:
    print("Selected video: " + videos[video_idx])

# import selected video:
selected_video = cv.VideoCapture(videos[video_idx])

# number of frames in video:
no_frames = count_frames(videos[video_idx], False)
#print(no_frames)
# play video:

while True:
    ret, frame = selected_video.read()              # read video frame by frame, ret == TRUE -> frame read successfully

    if (not ret):                                   # last frame was read
        print("Video stream completed - exiting.")
        break

    cv.imshow(videos[video_idx], frame)                 # display video frame by frame
    frame_counter = frame_counter + 1

    frame_ROI = frame[0:360, 110:640]
    if (XO.frameIsStatic(frame_ROI)):
        XO.detectShape(frame_ROI)                           # execute shape detection
        XO.detectGrid(frame_ROI)                            # execute grid detection
    cv.imshow("Analyzed video", frame)                 # display video frame by frame

    if ( frame_counter == no_frames ):
        cv.waitKey(0)                                   # hold at last frame until key is pressed
        break
    elif (cv.waitKey(50) & 0xff == ord('d')):           # wait 50ms after every frame displayed
        break

selected_video.release()
cv.destroyAllWindows()

