import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1])

K = np.array([
    [410.0,   0.0, 360.0],
    [  0.0, 410.0, 240.0],
    [  0.0,   0.0,   1.0]
])

D = np.array([
    [-0.085],
    [ 0.020],
    [-0.003],
    [ 0.0005]
])

DIM = (720, 480)

map1, map2 = cv2.fisheye.initUndistortRectifyMap(
    K,
    D,
    np.eye(3),
    K,
    DIM,
    cv2.CV_16SC2
)

undistorted = cv2.remap(
    img,
    map1,
    map2,
    interpolation=cv2.INTER_LINEAR,
    borderMode=cv2.BORDER_CONSTANT
)

cv2.imwrite("undistorted.jpg", undistorted)
