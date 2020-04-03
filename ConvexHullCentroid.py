import numpy as np
import cv2

img = cv2.imread('./tek2.png')
#Contours
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 20, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(str(len(contours)) + " contours found.")
cv2.drawContours(img, contours, -1, (0,255,255), 2)
for cnt in contours:
	#Moments
	M = cv2.moments(cnt)
	#print("M: " + str(M))
	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])
	#print("Centroid - cx: " + str(cx) + " cy: " + str(cy))

	#Convex Hull
	hullPoints = cv2.convexHull(cnt, returnPoints = True)
	hullIndices = cv2.convexHull(cnt, returnPoints = False)
	#print("Contour 0 points: " + str(cnt))
	#print("Convex Hull points: " + str(hullPoints))
	#print("Convex Hull indices: " + str(hullIndices)) #indexes of corresponding points in contours

	#Circle
	left_x = min(point[0][0] for point in hullPoints)
	bot_y = min(point[0][1] for point in hullPoints)
	right_x = max(point[0][0] for point in hullPoints)
	top_y = max(point[0][1] for point in hullPoints)
	width = max([right_x - left_x, top_y - bot_y])
	cv2.circle(img, (cx, cy), width // 2, (0, 0, 255), 2)
cv2.imshow('contours', img)
k = cv2.waitKey(0)
cv2.destroyAllWindows()