
# This entire script is for matplot lib. We can extend the same logic to openCV by detection methods
import GridPlot


# Initialzing starting point coordinates
sp1,sp2,sp3,sp4 = (480, 0),(540, 00),(600, 0),(660, 0)
# Initializing turning points coordinates for this configuration
tp1,tp2,tp3,tp4 = (480,480),(540,540),(600,540),(660,480)
# Initiazling final points for the bots to reach
fp1,fp2,fp3,fp4 = (0,480),(0,540),(1140,540),(1140,480)

coloursNormal = ((255,0,0),(0,255,0),(0,0,255),(255,255,0))
coloursInverted = ((50,255,255),(255,50,255),(255,255,50),(50,50,255))

colours =[coloursNormal,coloursInverted]

#List of points of current bots for plotting
InitialPoints =[sp1,sp2,sp3,sp4]
TurningPoints =[tp1,tp2,tp3,tp4]
FinalPoints   =[fp1,fp2,fp3,fp4]
Directions    =[1,1,0,0]  # 1 significies left and 0 significies right

im1 = GridPlot.MainGrid()
# im2 = GridPlot.PlotPosition(im1,InitialPoints)
# im3 = GridPlot.PlotPosition(im1,TurningPoints)
# im4 = GridPlot.PlotPosition(im1,FinalPoints)


RobNo = 4
imgArry=[]
for i in range(RobNo):
    startImg = GridPlot.PlotForwardPath(im1, InitialPoints[i], TurningPoints[i], FinalPoints[i],coloursNormal[i],Directions[i])
    imgArry += [startImg]
    endImg   = GridPlot.PlotReversePath(im1, InitialPoints[i], TurningPoints[i], FinalPoints[i],coloursInverted[i],Directions[i])
    imgArry += [endImg]
    
GridPlot.PlotImage(im1)
