# -*- coding: utf-8 -*-

import cv2
import imutils
import sys
from imutils.video import VideoStream
import time
import socket
import numpy as np
import requests

import encodings
serverName = '192.168.144.173'
serverPort = 12345
#create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#bind
server_socket.bind((serverName, serverPort ))

#listen
server_socket.listen(5)

client_socket, addr = server_socket.accept()
# sp1, sp2, sp3, sp4 = (480, 0), (540, 00), (600, 0), (660, 0)
# Initializing turning points coordinates for this configuration
tp1, tp2, tp3, tp4 = (480, 480), (540, 540), (600, 540), (660, 480)
# Initiazling final points for the bots to reach
fp1, fp2, fp3, fp4 = (0, 480), (0, 540), (1140, 540), (1140, 480)

# bot = 1
#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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


def moveForward(bot):
    # bot number, [forward = 1, rotate right = 2, rotate left = 3, stop and deliver package = 4]

    # tcpConnection(bot* 10 + 1, flag_send=1)
    print("Forward")


def rotateRight(bot):
    # tcpConnection(bot * 10 + 2, flag_send=1)
    print("turn right")


def rotateLeft(bot):
    # tcpConnection(bot * 10 + 3, flag_send=1)
    print('turn left')


def stopNDeliverPackage(bot):
    #tcpConnection(bot * 10 + 4, flag_send=1)
    print('deliver package')


turnedRight = False


def PlotForwardPath(image, startpoint, turnpoint, endpoint, direction, bot):
    # the point moves vertically down first and then chooses left or right
    x1, y1 = startpoint
    x2, y2 = endpoint
    a1, a2 = turnpoint
    global turnedRight
    if (x1 in range(x2 - 10, x2 + 10) and y1 in range(y2 - 10, y2 + 10)):
        print("Destination Reached!")
        stopNDeliverPackage(bot)
    if (y1 < a2) or turnedRight:
        # vertically moving pixelwise down
        moveForward(bot)
        return
    if (y1 >= a2) and direction:
        # vertically moving sidewise right
        turnedRight = True
        rotateRight(bot)
        moveForward(bot)
        return
    if (y1 >= a2) and not direction:
        # vertically moving sidewise left
        rotateLeft(bot)
        moveForward(bot)
        return


def PlotReversePath(image, startpoint, turnpoint, endpoint, direction, bot):
    # the point moves left or right first and then finally moves upwards
    x1, y1 = endpoint  # Actually this is the starting point
    x2, y2 = startpoint  # And this is the end point... i have interchanged because, i wanted the syntax to remain same
    a1, a2 = turnpoint

    if (x1 in range(x2 - 10, x2 + 10) and y1 in range(y2 - 10, y2 + 10)):
        start2 = False
        # stop()
        print("Initial Point Reached!")
        return True
    # if (x1 <= a1) and direction:
    #     # move right
    #     rotateRight(180)
    #     moveForward()
    #     return False
    # if (x1 > a1) and not direction:
    #     # move left
    #     rotateLeft(180)
    #     moveForward()
    #     return False
    if (x1 in range(a1 - 10, a1 + 10)):
        if (direction == 1):
            rotateLeft(bot)
            moveForward(bot)
            return False
        else:
            rotateRight(bot)
            moveForward(bot)
            return False

    if (y1 <= a2):
        # move top
        moveForward(bot)
        return False



def detect_video(frame, dict_type, robNo):
    if ARUCO_DICT.get(dict_type, None) is None:
        print("[INFO] ArUCo tag of '{}' is not supported".format(dict_type))
        sys.exit(0)
    # print("[INFO] detecting '{}' tags...".format(dict_type))
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[dict_type])
    arucoParams = cv2.aruco.DetectorParameters_create()

    # detect ArUco markers in the input frame
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame,
                                                       arucoDict, parameters=arucoParams)
    topLeft = 0 ,0
    arucoRobNo = [10, 20, 30, 40]
    if len(corners) > 0:

        ids = ids.flatten()

        for (markerCorner, markerID) in zip(corners, ids):
            # if markerID == arucoRobNo[robNo]:
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

    return frame, topLeft


def tcpConnection(data_to_send=0, flag_send=0):
    if flag_send:
        

        command_data = str(data_to_send)
        client_socket.send(command_data.encode('utf-8'))
        
        # data = client_socket.recv(1024)
    # else:
        # serverName = '192.168.43.52'
        # serverPort = 12345
        # client_socket.connect((serverName, serverPort))
        


def main():
    tcpConnection()
    
    #video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # InitialPoints = [sp1, sp2, sp3, sp4]
    TurningPoints = [tp1, tp2, tp3, tp4]
    FinalPoints = [fp1, fp2, fp3, fp4]
    Directions = [1, 1, 0, 0]  # 1 significies left and 0 significies right

    tcpConnection('f', 1)
    break_flag = 0

    bot = 1
    nextBot = False
    i, robNo = 0, 4
    url = "http://192.168.144.97:8080/shot.jpg"
    while i != robNo:
        while (1):
            #_, frame = video.read()
            img_resp = requests.get(url)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            frame = cv2.imdecode(img_arr, -1)
            frame = imutils.resize(frame, width=1000, height=1800)
            vid, topLeft = detect_video(frame, "DICT_5X5_50", i)
            # print(topLeft)

            bot = i+1
            if topLeft != (0, 0):
                PlotForwardPath(vid,topLeft, TurningPoints[i], FinalPoints[i],Directions[i], bot)
                nextBot = PlotReversePath(vid, topLeft, TurningPoints[i],FinalPoints[i],Directions[i], bot)

            if nextBot == True:
                i += 1
                break

            cv2.imshow("name", vid)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                global client_socket
                client_socket.close()
                break_flag = 1
                break

        if break_flag == 1:
            break
    video.release()
    cv2.destroyAllWindows()


main()
client_socket.close()
