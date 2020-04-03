import numpy as np
import cv2
import math

# parameters: define ranges of color in HSV
def showColor(lower_color, upper_color):
    img = cv2.imread('./tek2.png')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img,img, mask= mask)

    cv2.imshow('frame',img)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    k = cv2.waitKey(0)
    cv2.destroyAllWindows()

lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

lower_red1 = np.array([0,50,50])
upper_red1 = np.array([10,255,255])
lower_red2 = np.array([170,50,50])
upper_red2 = np.array([180,255,255])


lower_green = np.array([50,50,50])
upper_green = np.array([70,255,255])

#showColor(lower_blue, upper_blue)
showColor(lower_red, upper_red)
#showColor(lower_green, upper_green)