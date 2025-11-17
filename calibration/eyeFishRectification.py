## --- Turn into a class.
## --- And use as a stream for images

mport cv2
import numpy as np

# K and D from calibration
K = np.array([[fx, 0, cx],
              [0, fy, cy],
              [0,  0,  1]])

D = np.array([[k1], [k2], [k3], [k4]])

img = cv2.imread("fisheye.jpg")
h, w = img.shape[:2]

# Desired output matrix (usually same K or scaled)
new_K = K.copy()
new_K[0,0] = K[0,0]        # fx
new_K[1,1] = K[1,1]        # fy

# Compute mapping
map1, map2 = cv2.fisheye.initUndistortRectifyMap(
    K, D, np.eye(3), new_K, (w, h), cv2.CV_16SC2
)

undistorted = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR)

cv2.imwrite("undistorted.jpg", undistorted)
