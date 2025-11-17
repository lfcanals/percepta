import matplotlib.pyplot as plt
import numpy as np
import cv2



import numpy as np

def normalize_chessboard(corners, pattern_size):
    """
    corners: array Nx1x2 devuelto por findChessboardCorners
    pattern_size: (rows, cols) = (6,8) o lo que uses
    """

    rows, cols = pattern_size
    pts = corners.reshape(-1, 2)

    # Determinar si la geometría está (rows, cols) o (cols, rows)
    N = len(pts)
    if N != rows*cols:
        print("ERROR: número de puntos no coincide")
        return None

    # Caso 1: está rotado → mirar si la distancia entre puntos consecutivos crece en eje X o Y
    diff = pts[1] - pts[0]
    horizontal_layout = abs(diff[0]) > abs(diff[1])  # True = es 8 puntos por fila, False = 6

    if horizontal_layout:
        detected_cols = np.sum(np.isclose(pts[1:,0] - pts[:-1,0], diff[0], atol=20)) + 1
    else:
        detected_cols = np.sum(np.isclose(pts[1:,1] - pts[:-1,1], diff[1], atol=20)) + 1

    # Si detected_cols coincide con cols → ok
    # Si coincide con rows → está girado 90°/270° → rotar
    if detected_cols == cols:
        # -------- orientación correcta --------
        ordered = pts.reshape(rows, cols, 2)
    else:
        # -------- orientación 90° / 270° --------
        rotated = pts.reshape(cols, rows, 2)
        rotated = np.rot90(rotated, k=3)   # rotar 270° para alinear
        ordered = rotated

    # Asegurar que va de arriba-izq a abajo-der
    if ordered[0,0,0] > ordered[0,-1,0]:
        ordered = np.flip(ordered, axis=1)
    if ordered[0,0,1] > ordered[-1,0,1]:
        ordered = np.flip(ordered, axis=0)

    return ordered.reshape(-1,1,2).astype(np.float32)



class EyeFishCalibration:
    def __init__(self, checkBoardWidth=6, checkBoardHeight=8):
        self.CHECKERBOARD = (checkBoardWidth, checkBoardHeight) 
        cols = checkBoardWidth
        rows = checkBoardHeight
        #self.objp = np.zeros((1, rows * cols, 3), np.float32)
        #self.objp[0, :, :2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2)
        self.objp = np.zeros((1, rows*cols, 3), np.float32)
        self.objp[0, :, :2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2)


    def calculateParameters(self, images, imageNames=None):
        objpoints = []
        imgpoints = []

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
                corners_norm = normalize_chessboard(corners_refined, self.CHECKERBOARD)
                imgpoints.append(corners_refined)
                objpoints.append(self.objp.copy())

                #pts = corners_norm.reshape(-1,2)
                #for i in range(6):   # 6 filas si tu tablero es 6x8
                #    print(f"Row  {i}: x =", pts[i*8:(i+1)*8, 0])
                #print()

                #cv2.drawChessboardCorners(image, self.CHECKERBOARD, corners2, ret)
                #plt.imshow(image)
                #plt.show()
                #print(corners.shape)
            else:
                if(imageNames != None) : print(f'Discarded {imageNames[i]}')





        N_OK = len(objpoints)
        print(f"Using {N_OK} valid images of {len(images)}")

        img_shape = gray.shape[::-1]

        K = np.eye(3)
        D = np.zeros((4, 1))

        rvecs = []
        tvecs = []

        flags = (cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC +
                 #cv2.fisheye.CALIB_CHECK_COND +
                 cv2.fisheye.CALIB_FIX_SKEW)

        print("OBJ", objpoints[0].shape, objpoints[0].dtype)
        print("IMG", imgpoints[0].shape, imgpoints[0].dtype)

        rms, _, _, _, _ = cv2.fisheye.calibrate(
                objpoints, imgpoints, img_shape, K, D, rvecs, tvecs, flags,
                (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-6))

        return [K, D, rms]
