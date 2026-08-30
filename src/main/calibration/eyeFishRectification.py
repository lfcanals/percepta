import cv2
import numpy as np

class EyeFishRectification:
    def __init__(self, K, D):
        self.K = K
        self.D = D

        self.new_K = K.copy()
        self.new_K[0,0] = K[0,0]        # fx
        self.new_K[1,1] = K[1,1]        # fy

        self.eye3 = np.eye(3)


    def rectify(self, image):    
        """
            Rectifies an image.

            Args:
                image : a CV2 image

            Returns:
                rectified image
        """
        h, w = image.shape[:2]

        # Compute mapping
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(
            self.K, self.D, self.eye3, self.new_K, (w, h), cv2.CV_16SC2)

        return cv2.remap(image, map1, map2, interpolation=cv2.INTER_LINEAR)
