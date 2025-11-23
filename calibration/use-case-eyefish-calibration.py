from eyeFishCalibration import EyeFishCalibration
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import cv2

# 7 horiz x 9 vertical is 6x9 in the calibration language....
calibration = EyeFishCalibration(7, 7)

IMAGES_FOLDER = "test/calibration_chess/*.jpg"
imageNames = glob.glob(IMAGES_FOLDER)
images = []
for imageFile in imageNames:
    img = cv2.imread(imageFile)
    images.append(img)

K, D, error = calibration.runAll(images, imageNames)


print("error:", error)
print("K =\n", K)
print("D =\n", D)
