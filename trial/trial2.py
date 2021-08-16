
import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
import sys
import time
import stuff1

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
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

def MainGrid(size=(1200,600)):
    blank = np.zeros([size[1],size[0],3],dtype=np.uint8)
    blank.fill(255)
    img_3 = cv2.resize(blank, (1200, 600), interpolation = cv2.INTER_AREA)
    # plotting points
    color = (0,0,0)
    thickness = -1
    # bottom left
    start_point = (0, 420)
    end_point = (480, 480)
    img_3 = cv2.rectangle(img_3, start_point, end_point, color, thickness)
    # bottom right
    start_point = (720, 420)
    end_point = (1200, 480)
    img_3 = cv2.rectangle(img_3, start_point, end_point, color, thickness)
    # left pillar
    start_point = (420, 0)
    end_point = (480, 420)
    img_3 = cv2.rectangle(img_3, start_point, end_point, color, thickness)
    # right pillar
    start_point = (720, 0)
    end_point = (780, 420)
    img_3 = cv2.rectangle(img_3, start_point, end_point, color, thickness)

    #This function returns an image array that is plotted
    return img_3
    

def PlotPoint(points,colour):
    x1,y1 = (points[0],points[1])
    sp = (x1,y1)
    ep = (x1+60,y1+60)
    image = cv2.rectangle(MainGrid(),sp,ep,colour,-1)
    return image

def moveForward():
    print("F")
    pass
def rotateRight(x):
    print("rotr")
    pass
def rotateLeft(x):
    print('rotl')
    pass
    

def PlotForwardPath(image,startpoint,turnpoint,endpoint,colours,direction,shape='square'):
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
            moveForward()
            # direct = 2
            # image,(x1,y1) = PlotShape(MainGrid(),(x1,y1),direct,colours)
        if(y1>=a2) and direction:
            #vertically moving sidewise right
            rotateRight(90)
            moveForward()
        if(y1>=a2) and not direction:
            #vertically moving sidewise left
            rotateLeft(90)   
            moveForward()
        if(x1 in range(x2-10,x2+10) and y1  in range (y2-10,y2+10)):
            start = False
            # stop()
            print("Destination Reached!")
            return (x1,y1)
                  
    

def PlotReversePath(image,startpoint,turnpoint,endpoint,colours,direction,shape='square'):
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
        if(x1>a1) and not direction:
            #move left
            rotateLeft(180)
            moveForward()
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
        if(x1 in range(x2-10,x2+10) and y1  in range (y2-10,y2+10)):
            start2 = False
            # stop()
            print("Initial Point Reached!")
            return (x1,y1)
            

#detects colors in the images and puts bounding boxes in the image and return the position of the bot
def detect_object(frame,dict_type):
    if ARUCO_DICT.get(dict_type, None) is None:
        print("[INFO] ArUCo tag of '{}' is not supported".format(dict_type))
        sys.exit(0)
  
    print("[INFO] detecting '{}' tags...".format(dict_type))
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[dict_type])
    arucoParams = cv2.aruco.DetectorParameters_create()
    
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame,
                              arucoDict, parameters=arucoParams)
    
    if len(corners) > 0:
      
      ids = ids.flatten()
      print("in")
      
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
        # cv2.putText(frame, str(markerID),
        #   (topLeft[0], topLeft[1] - 15),
        #   cv2.FONT_HERSHEY_SIMPLEX,
        #   0.5, (0, 255, 0), 2)
        # cv2.putText(frame, str("corners"),
        #   (topLeft[0], topLeft[1] - 15),
        #   cv2.FONT_HERSHEY_SIMPLEX,
        #   0.5, (0, 255, 0), 2)
        
        # show the output frame
        # cv2.imshow("Frame", frame)
        # key = cv2.waitKey(1) & 0xFF
        # # if the `q` key was pressed, break from the loop
        # print('Hello')
        # if key == ord("q"):
          # break
        return frame,corners
    else:
        print("not working")

    # do a bit of cleanup
    cv2.destroyAllWindows()

def main():
    vid = cv2.VideoCapture(0)
    time.sleep(2.0)
    # img = cv2.resize(vid, (1200, 600))
    # Initialzing starting point coordinates
    sp1,sp2,sp3,sp4 = (480, 0),(540, 00),(600, 0),(660, 0)
    # Initializing turning points coordinates for this configuration
    tp1,tp2,tp3,tp4 = (480,480),(540,540),(600,540),(660,480)
    # Initiazling final points for the bots to reach
    fp1,fp2,fp3,fp4 = (0,480),(0,540),(1140,540),(1140,480)
    
    coloursNormal = ((100,100,0),(0,200,0),(0,0,200),(200,200,0))
    coloursInverted = ((50,255,255),(255,50,255),(255,255,50),(50,50,255))
    
    colours =[coloursNormal,coloursInverted]
    
    #List of points of current bots for plotting
    InitialPoints =[sp1,sp2,sp3,sp4]
    TurningPoints =[tp1,tp2,tp3,tp4]
    FinalPoints   =[fp1,fp2,fp3,fp4]
    Directions    =[1,1,0,0]  # 1 significies left and 0 significies right
    
    while(1):
        # RobNo=4
        # for i in range(RobNo):
            suc,frame = vid.read()
            if suc:
                print("calling fun")
                im,corners = detect_object(frame,'DICT_4X4_50')
                print("re")
                print(corners)
            else:
                print("gone")
            # x,y = [0],_[1]
            # (x1,y1)=PlotForwardPath(frame,InitialPoints[i], TurningPoints[i], FinalPoints[i],coloursNormal[i],Directions[i])
            # # img = PlotPoint((x1,y1),coloursNormal[i])
            # (x2,y2)=PlotReversePath(frame, InitialPoints[i], TurningPoints[i],(x1,y1),coloursNormal[i],Directions[i])
            # # img1= PlotPoint((x2,y2), coloursNormal[i])
            # # plt.imshow(img1)
            # # plt.show()
    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    print('Hello')
    if key == ord("q"):

    

main()
# stuff1.detect_video("DICT_5X5_50")