import cv2
import numpy as np
import matplotlib.pyplot as plt
#The functions in this module are:
    # MainGrid(size) Takes in the size and creates an image of flipkart challenge
    # InitPoints(image) Takes in image and plots initial positions of the robots
    # PlotImage(takes) Takes in an image and plots it in required dimensions
# A mere function to draw the plot with starting circles

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
    
def PlotPosition(image,points,radius=15,colours = ((255,0,0),(0,255,0),(0,0,255),(255,255,0))):
    # Points contains the corners of boxes of main plot
    # radius is set to default value of 15 pix, can be changed,
    # Colours contains a set of colours we want to plot the points with
    for i in range(len(points)):
        image =cv2.circle(image,(points[i][0],points[i][1]),radius,colours[i],-1)
    
    return image

def PlotImage(image):
    plt.title("Main Grid ")
    x_ticks = np.arange(0,1200,100)
    y_ticks = np.arange(0,600,100)
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)
    plt.imshow(image)
    plt.show()

def PlotForwardPath(image,startpoint,turnpoint,endpoint,colours,direction=1):
    #the point moves vertically down first and then chooses left or right
    x1,y1= startpoint
    x2,y2= endpoint
    a1,a2= turnpoint
    start = True
    while(start):
        if(y1<a2):
            #vertically moving pixelwise down
            #we can write an opencv function here if we want
            y1 = y1+60
            stp = (x1+30,y1)
            spp = (x1+30,y1+60)
            image = cv2.line(image,stp,spp,colours,2)
        if(y1>=a2) and direction:
            #vertically moving sidewise right
            x1 = x1-60
            stp2 = (x1+60,y1+30)
            spp2 = (x1,y1+30)
            image = cv2.line(image,stp2,spp2,colours,4)
        if(y1>=a2) and not direction:
            #vertically moving sidewise left
            x1 = x1+60
            spp1 = (x1+60,y1+30)
            stp1 = (x1,y1+30)
            image = cv2.line(image,stp1,spp1,colours,4)
        if(x1 == x2 and y1 == y2):
            start = False
    
    return image

def PlotReversePath(image,startpoint,turnpoint,endpoint,colours,direction=1):
    # the point moves left or right first and then finally moves upwards
    x1,y1= endpoint
    x2,y2= startpoint
    a1,a2= turnpoint
    start1 = True
    while(start1):
        if(x1 <= a1) and direction:
            # moving right
            x1=x1+60
            stp1 = (x1,y1+40)
            spp1 = (x1+60,y1+40)
            image = cv2.line(image,stp1,spp1,colours,2)
        if(x1>a1) and not direction:
            # moving left
            x1 = x1-60
            stp2 = (x1+60,y1+40)
            spp2 = (x1,y1+40)
            image = cv2.line(image,stp2,spp2,colours,2)
        if(x1 == a1):
            start1= False
    start2 = True
    while(start2):
        if(y1<=a2):
            y1 = y1-60
            stp = (x1+40,y1)
            spp = (x1+40,y1-60)
            image = cv2.line(image,stp,spp,colours,2)
        if(x1 == x2 and y1 == y2):
            start2 = False
    
    return image
            
            
    
