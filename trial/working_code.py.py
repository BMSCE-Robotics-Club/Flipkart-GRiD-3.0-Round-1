# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 17:54:45 2021

@author: FranticUser
"""

import cv2
import imutils
import sys
from imutils.video import VideoStream
import time

sp1,sp2,sp3,sp4 = (480, 0),(540, 00),(600, 0),(660, 0)
# Initializing turning points coordinates for this configuration
tp1,tp2,tp3,tp4 = (480,480),(540,540),(600,540),(660,480)
# Initiazling final points for the bots to reach
fp1,fp2,fp3,fp4 = (0,480),(0,540),(1140,540),(1140,480)


ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000
}

def moveForward():
    print("F")
def rotateRight(x):
    print("rotr")
def rotateLeft(x):
    print('rotl')

def PlotForwardPath(image,startpoint,turnpoint,endpoint,direction):
    #the point moves vertically down first and then chooses left or right
    x1,y1= startpoint
    x2,y2= endpoint
    a1,a2= turnpoint
    start = True
    #direct = (1,2,3,4) map respectively to (up,down,left, right)
    while(start):
        if(y1<a2):
            #vertically moving pixelwise down
            #we can write an opencv function here if we want
            y1 = y1+60
            moveForward()
        if(y1>=a2) and direction:
            #vertically moving sidewise right
            rotateRight(90)
            moveForward()
            x1 = x1-30
        if(y1>=a2) and not direction:
            #vertically moving sidewise left
            rotateLeft(90)   
            moveForward()
            x1 = x1+30
        if(x1 in range(x2-10,x2+10) and y1  in range (y2-10,y2+10)):
            start = False
            # stop()
            print("Destination Reached!")
            return (x1,y1)

def PlotReversePath(image,startpoint,turnpoint,endpoint,direction):
    # the point moves left or right first and then finally moves upwards
    x1,y1= endpoint   # Actually this is the starting point
    x2,y2= startpoint # And this is the end point... i have interchanged because, i wanted the syntax to remain same
    a1,a2= turnpoint
    start1 = True
    while(start1):
        if(x1 <= a1) and direction:
            #move right
            rotateRight(180)
            moveForward()
            x1 = x1-60
        if(x1>a1) and not direction:
            #move left
            rotateLeft(180)
            moveForward()
            x1 = x1+60
        if(x1 in range(a1-10,a1+10)):
            if(direction==1):
                rotateLeft(90)
            else:
                rotateRight(90)
                
            # stop()
            
    start2 = True
    while(start2):
        if(y1<=a2):
            #move top
            moveForward()
            y1 = y1-60
        if(x1 in range(x2-10,x2+10) and y1  in range (y2-10,y2+10)):
            start2 = False
            # stop()
            print("Initial Point Reached!")
            return (x1,y1)
        

def detect_video(frame,dict_type):
    if ARUCO_DICT.get(dict_type, None) is None:
        print("[INFO] ArUCo tag of '{}' is not supported".format(dict_type))
        sys.exit(0)
    print("[INFO] detecting '{}' tags...".format(dict_type))
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[dict_type])
    arucoParams = cv2.aruco.DetectorParameters_create()
    
    # detect ArUco markers in the input frame
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame,
                              arucoDict, parameters=arucoParams)
    print("Working till here!")
    
    if len(corners) > 0:
    
        ids = ids.flatten()
    
        for (markerCorner, markerID) in zip(corners, ids):
          # extract the marker corners 
          corners = markerCorner.reshape((4, 2))
          (topLeft, topRight, bottomRight, bottomLeft) = corners
          # convert each of the (x, y)-coordinate pairs to integers
          topRight = (int(topRight[0]), int(topRight[1]))
          bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
          bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
          topLeft = (int(topLeft[0]), int(topLeft[1]))
    
          # draw the bounding box of the ArUCo detection
          cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
          cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
          cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
          cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
          # compute and draw the center (x, y)-coordinates of the
          # ArUco marker
          cX = int((topLeft[0] + bottomRight[0]) / 2.0)
          cY = int((topLeft[1] + bottomRight[1]) / 2.0)
          cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
          # draw the ArUco marker ID on the frame
          cv2.putText(frame, str(markerID),
            (topLeft[0], topLeft[1] - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 255, 0), 2)
          
    return frame
  

def main():
    video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    InitialPoints =[sp1,sp2,sp3,sp4]
    TurningPoints =[tp1,tp2,tp3,tp4]
    FinalPoints   =[fp1,fp2,fp3,fp4]
    Directions    =[1,1,0,0]  # 1 significies left and 0 significies right
    
    while(1):
        _,frame = video.read()
        vid = detect_video(frame,"DICT_5X5_100")
        robNo=4
        # for i in range(robNo):
        #     (x1,y1)=PlotForwardPath(vid,InitialPoints[0], TurningPoints[0], FinalPoints[0],Directions[0])
        #     print("String works",x1,y1)
        #     (x2,y2)=PlotReversePath(vid, InitialPoints[0], TurningPoints[0],FinalPoints[0],Directions[0])
        #     print("Second string also works!",x2,y2)
        
        cv2.imshow("name",vid)
        if cv2.waitKey(1) &  0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()

main()