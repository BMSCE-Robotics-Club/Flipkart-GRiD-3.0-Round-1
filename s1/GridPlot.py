# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 13:44:58 2021

@author: FranticUser
"""

''' Legacy Movements Code Don't change! Just for reference:
    Move Right:
             x1=x1+60
            stp1 = (x1,y1+30)
            spp1 = (x1+60,y1+30)
            image = cv2.line(image,stp1,spp1,colours,2)      
            
    Move Left:
            x1 = x1-60
            stp2 = (x1+60,y1+30)
            spp2 = (x1,y1+30)
            image = cv2.line(image,stp2,spp2,colours,2)
    '''
import cv2
import numpy as np
import matplotlib.pyplot as plt
#The functions in this module are:
    # MainGrid(size) Takes in the size and creates an image of flipkart challenge
    # PlotPosition() Given a tuple containing positions of all four bots, it plots them only used if initial and final conditions are known
    # PlotPoint() Given a single set of points(x1,y1) points a cv2 box from it
    # PlotShape() Used by Forward and Reverse path, has option to draw line if 'line' is given as for input of shape
    # PlotForwardPath() Given Initial point, endpoint and turning points, it plots out in a L shaped manner
    # PlotReversePath() Given initial point, endpoint and turning points, albeit in reverse order, it plots reverse path
    #       Be careful with this function do not change without understanding the code!!
    # detect_color() Takes a given input numpy array and finds out the shape present and the colour of it. It's still a work in progress
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
    
def PlotPositions(image,points,radius=15,colours = ((255,0,0),(0,255,0),(0,0,255),(255,255,0))):
    # Points contains the corners of boxes of main plot
    # radius is set to default value of 15 pix, can be changed,
    # Colours contains a set of colours we want to plot the points with
    for i in range(len(points)):
        # uncomment these for rectangular plots
        # sp =(points[i][0],points[i][1])
        # ep =(points[i][0]+60,points[i][1]+60)
        # #image =cv2.rectangle(image,sp,ep,colours[i],-1)
        
        #uncomment these for circular plots
        center=(points[i][0]+30,points[i][1]+30)
        image =cv2.circle(image,center,radius,colours[i],-1)
    return image

def PlotPoint(points,colour):
    x1,y1 = (points[0],points[1])
    sp = (x1,y1)
    ep = (x1+60,y1+60)
    image = cv2.rectangle(MainGrid(),sp,ep,colour,-1)
    return image

    
def PlotShape(image,points,direction,colours,shape='square'):
    x1,y1 = (points[0],points[1])
    if(direction ==1):
        y1 = y1-60
        if shape == 'line':
        #for plotting line
            stp = (x1+40,y1)
            spp = (x1+40,y1-60)
            image = cv2.line(image,stp,spp,colours,2)
        if shape == 'square':
        #for plotting rectangle box
            sp=(x1,y1)
            ep=(x1+60,y1+60)
            image = cv2.rectangle(image,sp,ep,colours,-1)
            _,__,image = detect_color(image)
        return image,(x1,y1)
    
    if(direction == 2):
        y1 = y1+60
        if shape == 'line':
            stp = (x1+30,y1)
            spp = (x1+30,y1+60)
            image = cv2.line(image,stp,spp,colours,2)
        
        if shape == 'square':
        #for plotting rectangle box
            sp=(x1,y1)
            ep=(x1+60,y1+60)
            image = cv2.rectangle(image,sp,ep,colours,-1)
            _,__,image = detect_color(image)
        return image,(x1,y1)
    if(direction == 4):
        x1 = x1-60
        if shape == 'line':
            stp2 = (x1+60,y1+30)
            spp2 = (x1,y1+30)
            image = cv2.line(image,stp2,spp2,colours,4)
        
        if shape == 'square':
        #for plotting rectangle box
            sp=(x1,y1)
            ep=(x1+60,y1+60)
            image = cv2.rectangle(image,sp,ep,colours,-1)
            _,__,image = detect_color(image)
        return image,(x1,y1)
    
    if(direction == 3):
        x1 = x1+60
        if shape == 'line':
            spp1 = (x1+60,y1+30)
            stp1 = (x1,y1+30)
            image = cv2.line(image,stp1,spp1,colours,4)

        if shape == 'square':
        #for plotting rectangle box
            sp=(x1,y1)
            ep=(x1+60,y1+60)
            image = cv2.rectangle(image,sp,ep,colours,-1)
            _,__,image = detect_color(image)
        return image,(x1,y1)
    

def PlotForwardPath(image,startpoint,turnpoint,endpoint,colours,direction,shape='square'):
    #the point moves vertically down first and then chooses left or right
    x1,y1= startpoint
    x2,y2= endpoint
    a1,a2= turnpoint
    start = True
    #direct = (1,2,3,4) map respectively to (up,down,left, right)
    while(start):
        if(y1<=a2):
            #vertically moving pixelwise down
            #we can write an opencv function here if we want
            direct = 2
            image,(x1,y1) = PlotShape(MainGrid(),(x1,y1),direct,colours)
        if(y1>a2) and not direction:
            #vertically moving sidewise right
            direct = 4
            image,(x1,y1) = PlotShape(MainGrid(),(x1,y1),direct,colours)
        if(y1>a2) and not direction:
            #vertically moving sidewise left
            direct = 3
            image,(x1,y1) = PlotShape(MainGrid(),(x1,y1),direct,colours)
        if x1 in range(a2-10,a2+10):
            PlotPoint((x1,y1), colours)        
        if(x1 in range(x2-10,x2+10) and y1  in range (y2-10,y2+10)):
            start = False
            print("Destination Reached!")
            return (x1,y1)
                   
        plt.imshow(image)
        plt.show(block=False)
        plt.pause(0.05)
        plt.close()
    

def PlotReversePath(image,startpoint,turnpoint,endpoint,colours,direction,shape='square'):
    # the point moves left or right first and then finally moves upwards
    x1,y1= endpoint   # Actually this is the starting point
    x2,y2= startpoint # And this is the end point... i have interchanged because, i wanted the syntax to remain same
    a1,a2= turnpoint
    start1 = True
    while(start1):
        if(x1 <= a1) and direction:
            #move right
            direct = 3
            image,(x1,y1) = PlotShape(MainGrid(),(x1,y1),direct,colours)
        if(x1>a1) and not direction:
            #move left
            direct = 4
            image,(x1,y1) = PlotShape(MainGrid(),(x1,y1),direct,colours)
        if(x1 in range(a1-10,a1+10)):
            start1= False
            
        plt.imshow(image)
        plt.show(block=False)
        plt.pause(0.05)
        plt.close()
    start2 = True
    while(start2):
        if(y1<=a2):
            #move top
            direct =1
            image,(x1,y1) = PlotShape(MainGrid(),(x1,y1),direct,colours)
        if(x1 in range(x2-10,x2+10) and y1  in range (y2-10,y2+10)):
            start2 = False
            print("Initial Point Reached!")
            return (x1,y1)
        plt.imshow(image)
        plt.show(block=False)
        plt.pause(0.05)
        plt.close()
            

#detects colors in the images and puts bounding boxes in the image and return the position of the bot
def detect_color(frame):
    # Converts images from BGR to HSV It is very much required...! Cause we are transfering matplotlib to csv
    hsv1=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(hsv1, cv2.COLOR_BGR2HSV)
    kernal = np.ones((5, 5), "uint8")
    
    
    blue_lower = np.array([94, 80, 72], np.uint8)
    blue_upper = np.array([128, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(frame, frame, mask = blue_mask)


    red_lower = np.array([156, 50, 71], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(frame, frame, mask = red_mask)
    # Set range for green color and
    # define mask
    green_lower = np.array([36, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(frame, frame, mask = green_mask)
    
    yellow_lower = np.array([25, 50, 70], np.uint8)
    yellow_upper = np.array([35, 255, 255], np.uint8)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    yellow_mask = cv2.dilate(yellow_mask, kernal)
    res_yellow = cv2.bitwise_and(frame, frame, mask = yellow_mask)

    # Creating contour to track blue color
    contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 1):
            x, y, w, h = cv2.boundingRect(contour)
            print(str(x) + " " + str(y) + " Blue")
            color = "Blue"
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "Blue Colour", (x+60, y+60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0))
    
    contours, hierarchy = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 1):
            x, y, w, h = cv2.boundingRect(contour)
            print(str(x) + " " + str(y) + " Yellow")
            color = "Yellow"
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv2.putText(frame, "Yellow Colour", (x+60, y+60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0))

    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 1):
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            print(str(x) + " " + str(y) + " Red")
            cv2.putText(frame, "Red Colour", (x+60, y+60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 1):
            x, y, w, h = cv2.boundingRect(contour)
            color = "Green"
            print(str(x) + " " + str(y) + " Green")
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Green Colour", (x+60, y+60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (27, 255, 0))
    

    return (x,y,w,h),color,frame
