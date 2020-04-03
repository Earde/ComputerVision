import numpy as np
import cv2
import math

img = cv2.imread('./bouten_moeren2.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
grayBlur = cv2.GaussianBlur(gray, (25,25), 0)
ret,th=cv2.threshold(grayBlur, 180, 255, cv2.THRESH_BINARY_INV)
contours, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

thresholdRedelijkRond = 0.5
thresholdErgRond = 0.8
thresholdTeRond = 0.90

thresholdVeelGaten = 50

hierarchy = hierarchy[0]
for cnr in range(len(contours)):
    cnt = contours[cnr]
    area = cv2.contourArea(cnt)
    # teken alleen contouren met een oppervlakte groter dan 100
    if area > 100:
        #bereken de cirkel factor
        perimeter = cv2.arcLength(cnt, True)
        factor = 4 * math.pi * area / perimeter ** 2
        #kijk of er nog meer contouren binnen dit contour vallen (parent-child hierarchy)
        holes = 0
        child = hierarchy[cnr][2]
        while child >= 0:
            holes += cv2.contourArea(contours[child])
            child = hierarchy[child][0]
        #klassificeer de bouten en moeren
        if factor > thresholdTeRond:#binnenste cirkel van liggende moer (veel te rond)
            continue
        elif factor < thresholdRedelijkRond and holes is 0: #liggende bout (niet rond, zonder gaten)
            cv2.drawContours(img, [cnt], -1, (0,255,255), 3)
        elif factor > thresholdErgRond and holes < thresholdVeelGaten: #staande bout (erg rond, met weinig gaten)
            cv2.drawContours(img, [cnt], -1, (100,200,0), 3)
        elif factor > thresholdRedelijkRond and holes > thresholdVeelGaten:#liggende moer(redelijk rond, met veel gaten)
            cv2.drawContours(img, [cnt], -1, (255,0,0), 3)
        elif factor > thresholdRedelijkRond and holes is 0:#staande moer(redelijk rond, zonder gaten)
            cv2.drawContours(img, [cnt], -1, (255,0,250), 3)
        print("Area: " + str(area) + " Factor: " + str(factor) + "Holes: " + str(holes))

cv2.imshow('contours', img)
k = cv2.waitKey(0)
cv2.destroyAllWindows()