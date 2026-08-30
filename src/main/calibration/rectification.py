import cv2
import numpy as np

# K and D from calibration
K = np.array([[287.76591116,0., 345.20926163],
 [  0.,        340.70870078,249.21151386],
 [  0.,           0.,          1.        ]])
D = np.array([[ 0.09877731],
 [-0.18884432],
 [ 0.15823933],
 [-0.04348117]])

i=1
while i<=4:
    img = cv2.imread("test/fisheye" + str(i) + ".jpg")
    h, w = img.shape[:2]

    # Desired output matrix (usually same K or scaled)
    new_K = K.copy()
    new_K[0,0] = K[0,0]        # fx
    new_K[1,1] = K[1,1]        # fy

    # Compute mapping
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(
        K, D, np.eye(3), new_K, (w, h), cv2.CV_16SC2)

    undistorted = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR)

    cv2.imwrite("undistorted" + str(i) + ".jpg", undistorted)
    i=i+1
