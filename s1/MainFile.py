# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 14:23:52 2021

@author: FranticUser
"""

# This entire script is for matplot lib. We can extend the same logic to openCV by detection methods
import matplotlib.pyplot as plt
import GridPlot

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

im1 = GridPlot.MainGrid()
im2 = GridPlot.PlotPositions(im1,InitialPoints)
im3 = GridPlot.PlotPositions(im1,TurningPoints)
im4 = GridPlot.PlotPositions(im1,FinalPoints)
plt.imshow(im4)
print('Initial,final and turning points')
plt.pause(1)
print('The Algorithm is going to begin now')
plt.close()


RobNo=4
for i in range(RobNo):
    im =GridPlot.PlotPoint(InitialPoints[i],coloursNormal[i])
    _,__,im = GridPlot.detect_color(im)
    x,y = _[0],_[1]
    plt.imshow(im)
    plt.show()
    (x1,y1)=GridPlot.PlotForwardPath( GridPlot.MainGrid(),InitialPoints[i], TurningPoints[i], FinalPoints[i],coloursNormal[i],Directions[i])
    img = GridPlot.PlotPoint((x1,y1),coloursNormal[i])
    plt.imshow(img)
    plt.show()
    (x2,y2)=GridPlot.PlotReversePath( GridPlot.MainGrid(), InitialPoints[i], TurningPoints[i],(x1,y1),coloursNormal[i],Directions[i])
    img1= GridPlot.PlotPoint((x2,y2), coloursNormal[i])
    plt.imshow(img1)
    plt.show()
