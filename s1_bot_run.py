import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt
import time

"""
scale
5ft x 12 x 10 = 600 px
10ft x  12 x 10 = 1200 px
line thickness -> 0.393701 x 10 = 4px
"""

# generates a image of the grid without the bot
def new_image():
    blank = np.zeros([600,1200,3],dtype=np.uint8)
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
    return cv2.rectangle(img_3, start_point, end_point, color, thickness)

#detects colors in the images and puts bounding boxes in the image and return the position of the bot
def detect_color(frame):
    # Converts images from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    kernal = np.ones((5, 5), "uint8")
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(frame, frame, mask = blue_mask)

    contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 1):
            x, y, w, h = cv2.boundingRect(contour)
            print(str(x) + " " + str(y) + " Blue")
            color = "Blue"
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "Blue Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0))

    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsv, red_lower, red_upper)

    # Set range for green color and
    # define mask
    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)

    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(frame, frame, mask = red_mask)

    # For green color
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(frame, frame, mask = green_mask)

    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 1):
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            print(str(x) + " " + str(y) + " Red")
            cv2.putText(frame, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 1):
            x, y, w, h = cv2.boundingRect(contour)
            color = "Green"
            print(str(x) + " " + str(y) + " Green")
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Green Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))

    return x,y,w,h,color,frame


def move_bot():
    # placing s1 in the initial position
    thickness = -1
    red = (0,90,0)
    destination = (0, 480)
    start_point = (480, 0)
    end_point = (540, 60)
    frame = cv2.rectangle(new_image(), start_point, end_point, red, thickness)
    flag = 0
    plt.imshow(detect_color(frame)[-1])
    plt.show(block=False)
    plt.pause(1)
    plt.close()

    while(1):
        # detect color and get current position of the bot and put bounding boxes
        vals = detect_color(frame)
        # vertical movement
        if(vals[1] < destination[1] and flag == 0):
            # updating the new position of the bot
            start_point = (start_point[0], start_point[1] + 60)
            end_point = (start_point[0] + 60, start_point[1] + 60)
            frame = cv2.rectangle(new_image(), start_point, end_point, red, thickness)
            # checking if it reached the bottom most point
            if(end_point[1] == 540):
                flag = 1
                plt.imshow(detect_color(frame)[-1])
                plt.show(block=False)
                plt.pause(1)
                plt.close()
                continue

        # horizontal movement
        if(flag == 1 and vals[0] > destination[0]-10):
            # updating the new position of the bot
            start_point = (start_point[0] - 60, start_point[1])
            end_point = (start_point[0] + 60, start_point[1] + 60)
            frame = cv2.rectangle(new_image(), start_point, end_point, red, thickness)
            # checking if it reached the destination
            if(end_point[1] == 120): break

        plt.imshow(detect_color(frame)[-1])
        plt.show(block=False)
        plt.pause(1)
        plt.close()

move_bot()
