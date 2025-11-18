import matplotlib.pyplot as plt
import numpy as np
import cv2



import numpy as np


class EyeFishCalibration:
    def __init__(self, checkBoardWidth=6, checkBoardHeight=8):
        self.CHECKERBOARD = (checkBoardWidth, checkBoardHeight) 
        cols = checkBoardWidth
        rows = checkBoardHeight
        self.objp = np.zeros((1, rows*cols, 3), np.float32)
        self.objp[0, :, :2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2)

        self.objpoints = []
        self.imgpoints = []

        self.K = None
        self.D = None


    def calculateParameters(self, images, imageNames=None):
        i=-1
        for image in images:
            i=i+1
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, self.CHECKERBOARD,
                    cv2.CALIB_CB_ADAPTIVE_THRESH #+ cv2.CALIB_CB_FAST_CHECK 
                    + cv2.CALIB_CB_NORMALIZE_IMAGE)

            if ret:
                corners_refined = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1),
                        criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 
                        30, 0.001))
                corners_norm = self.normalize_chessboard(corners_refined)
                self.imgpoints.append(corners_refined)
                self.objpoints.append(self.objp.copy())

            else:
                if(imageNames != None) : print(f'Discarded {imageNames[i]}')




        N_OK = len(self.objpoints)
        print(f"Using {N_OK} valid images of {len(images)}")

        img_shape = gray.shape[::-1]

        flags = (cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC +
                 #cv2.fisheye.CALIB_CHECK_COND +
                 cv2.fisheye.CALIB_FIX_SKEW)

        if self.K is not None:
             flags |= cv2.fisheye.CALIB_USE_INTRINSIC_GUESS

        #print("OBJ", objpoints[0].shape, objpoints[0].dtype)
        #print("IMG", imgpoints[0].shape, imgpoints[0].dtype)

        rvecs = []
        tvecs = []
        rms, _, _, _, _ = cv2.fisheye.calibrate(
                self.objpoints, self.imgpoints, img_shape, self.K, self.D, 
                rvecs, tvecs, flags,
                (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-6))

        return [self.K, self.D, rms]


    def normalize_chessboard(self, corners):
        """
        corners: array Nx1x2 devuelto por findChessboardCorners
        pattern_size: (rows, cols) = (6,8) o lo que uses
        """
    
        rows, cols = self.CHECKERBOARD
        pts = corners.reshape(-1, 2)
    
        N = len(pts)
        if N != rows*cols:
            print("ERROR: número de puntos no coincide")
            return None
    
        # Check if distance between the to first points is mainly in X or Y
        diff = pts[1] - pts[0]
        horizontal_layout = abs(diff[0]) > abs(diff[1])  
    
        if horizontal_layout:
            detected_cols = np.sum(np.isclose(pts[1:,0] - pts[:-1,0], diff[0], atol=20)) + 1
        else:
            detected_cols = np.sum(np.isclose(pts[1:,1] - pts[:-1,1], diff[1], atol=20)) + 1
    
        if detected_cols == cols:
            # -------- correct orientation --------
            ordered = pts.reshape(rows, cols, 2)
        else:
            # -------- rotated 90° / 270° --------
            rotated = pts.reshape(cols, rows, 2)
            rotated = np.rot90(rotated, k=3)   # rotate 270°
            ordered = rotated
    
        # Be sure that it's properly ordered
        if ordered[0,0,0] > ordered[0,-1,0]:
            ordered = np.flip(ordered, axis=1)
        if ordered[0,0,1] > ordered[-1,0,1]:
            ordered = np.flip(ordered, axis=0)
    
        return ordered.reshape(-1,1,2).astype(np.float32)
    
    
    
