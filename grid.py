import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt

"""
scale
5ft x 12 x 10 = 600 px
10ft x  12 x 10 = 1200 px
line thickness -> 0.393701 x 10 = 4px
"""

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
img_3 = cv2.rectangle(img_3, start_point, end_point, color, thickness)

# s1
red = (255,0,0)
start_point = (480, 0)
end_point = (540, 60)
img_3 = cv2.rectangle(img_3, start_point, end_point, red, thickness)

# predict path for s1
status = True
s1_y = 0
s1_x = 480
while(status):
    # vertical transition
    if(s1_y<480):
        # bot has to move vertically downwards
        s1_y = s1_y + 60
        start_point = (s1_x, s1_y)
        end_point = (s1_x + 60, s1_y + 60)
        img_3 = cv2.rectangle(img_3, start_point, end_point, red, thickness)
    if(s1_y >= 480):
        # bot has to move horizontally towards left
        s1_x = s1_x - 60
        start_point = (s1_x, s1_y)
        end_point = (s1_x + 60, s1_y + 60)
        img_3 = cv2.rectangle(img_3, start_point, end_point, red, thickness)
        # bot reaching destination
    if(s1_x == 0 and s1_y == 480):
        status = False

plt.title("Flipkart Grid - S1 -> vertically down dist = " + str(480/120) + "ft horizontally leftwards = " + str(480/120) + "ft")
x_ticks = np.arange(0, 1200, 60)
plt.xticks(x_ticks)
y_ticks = np.arange(0, 600, 60)
plt.yticks(y_ticks)
plt.grid()

plt.imshow(img_3)
print("image shape: ", img_3.shape)
plt.show()
