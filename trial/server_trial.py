import socket
import time
import cv2 
import sys

ARUCO_DICT = {
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
}

def move_socket(x,s,close_flag=0):
    client, addr = s.accept()
    if close_flag:
        client.close()
    else:
        client.send(bytes(x, 'utf-8'))
    #client.settimeout(5)
    
    
def detect_video(frame, dict_type):
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

    return frame, topLeft

def main():
    #initializing the socket and getting the ip address
    close_flag=0
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print('My IP: '+IPAddr)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IPAddr, 8585 ))
    s.listen(0)                 
    
    #capturing video
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while (1):
        _, frame = video.read()
        vid, topLeft = detect_video(frame, "DICT_5X5_100")
        print(topLeft)
        cv2.imshow('before',vid)
        if topLeft != (0,0):
            if topLeft[1] <300:
                print('f')
                # move_socket('f',s)
            else:
                print('s')
                # move_socket('s',s)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            close_flag=1
            # move_socket('s',s,close_flag)
            break
        
    video.release()
    cv2.destroyAllWindows()
    

main()      
