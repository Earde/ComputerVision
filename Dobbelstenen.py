import numpy as np
import cv2
import math

def processDie(die, num):
    eyes = 0
    #vormfactor threshold
    thresholdIsRound = 0.8
    #pas blurren en thresholden toe
    grayBlur = cv2.GaussianBlur(die, (15, 15), 0)
    ret,th=cv2.threshold(grayBlur, 225, 255, cv2.THRESH_BINARY_INV)
    #loop door alle contouren heen
    contours, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = hierarchy[0]
    for cnr in range(len(contours)):
        cnt = contours[cnr]
        area = cv2.contourArea(cnt)
        if area > 10:#de cirkel moet wel een minimale grootte hebben anders werken de berekeningen hieronder niet 
            #bereken de cirkel factor
            perimeter = cv2.arcLength(cnt, True)
            factor = 4 * math.pi * area / perimeter ** 2
            #vind de ogen van de dobbelsteen
            if factor > thresholdIsRound:
                eyes += 1
                cv2.drawContours(die, [cnt], -1, (0, 0, 255), 3)
                #print("Area: " + str(area) + " Factor: " + str(factor) + "Holes: " + str(holes))
    cv2.imshow('die ' + str(num), die)
    return eyes
            
img = cv2.imread('./dobbelstenen.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
grayBlur = cv2.GaussianBlur(gray, (11,11), 0)
ret,th=cv2.threshold(grayBlur, 20, 255, cv2.THRESH_BINARY_INV)
contours, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

totalEyes = []

hierarchy = hierarchy[0]
for cnr in range(len(contours)):
    cnt = contours[cnr]
    area = cv2.contourArea(cnt)
    if area > 2000 and area < 10000: #is een dobbelsteen
        cv2.drawContours(img, [cnt], -1, (0,0,255), 3)
        #snijd dubbelsteen gedeelte eruit en handel deze af
        x,y,w,h = cv2.boundingRect(cnt)
        die = gray[y:y+h, x:x+w]
        totalEyes.append(processDie(die, cnr))
totalEyes.sort()
print(totalEyes)
#cv2.imshow('contours25', grayBlur25)
cv2.imshow('dice', img)
k = cv2.waitKey(0)
cv2.destroyAllWindows()