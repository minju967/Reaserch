import cv2
import numpy as np
from scipy.ndimage import label

img = cv2.imread('C:\\Users\\user\\PycharmProjects\\Reaserch\\obj_depth\\K110303_214_005.png')
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thr = cv2.threshold(imgray, 170, 0, cv2.THRESH_TOZERO)

cv2.imshow('thr', thr)
cv2.waitKey(0)
cv2.destroyAllWindows()

kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel, iterations=2)

border = cv2.dilate(opening, kernel, iterations=3)
border = border - cv2.erode(border, None)

dt = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
dt = ((dt-dt.min())/(dt.max()-dt.min())*255).astype(np.uint8)
_, dt = cv2.threshold(dt, 180, 255, cv2.THRESH_BINARY)

marker, ncc = label(dt)
marker = marker*(255/ncc)

marker[border == 255] = 255
marker = marker.astype(np.int32)
cv2.watershed(img, marker)

marker[marker == -1] = 0
marker = marker.astype(np.uint8)
marker = 255 - marker

marker[marker != 255] = 0
marker = cv2.dilate(marker, None)
img[marker == 255] = (0, 0, 255)

cv2.imshow('watershed', img)
cv2.waitKey(0)
cv2.destroyAllWindows()