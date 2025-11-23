from eyeFishCalibration import EyeFishCalibration
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import cv2

# 7 horiz x 9 vertical is 6x9 in the calibration language....
calibration = EyeFishCalibration(7, 7)

IMAGES_FOLDER = "test/calibration_chess/*.jpg"
imageNames = glob.glob(IMAGES_FOLDER)
i = 0
images = []
for imageFile in imageNames:
    #print(imageFile)
    img = cv2.imread(imageFile)
    images.append(img)
    if len(images)>10:
        K, D, error = calibration.runAll(images, imageNames)
        images = []


if len(images)>0:
    K, D, error = calibration.runAll(images, imageNames)
print("error:", error)
print("K =\n", K)
print("D =\n", D)
