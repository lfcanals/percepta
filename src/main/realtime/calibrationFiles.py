import json
import numpy as np


calibrationFile = '../database/calibration-camera.json'
leftLineFile = '../database/lane-calibration-left.json'
rightLineFile = '../database/lane-calibration-right.json'


def writeEyeFishCalibration(incrementalCalibration):
    data={}
    data = {}
    data['K'] = incrementalCalibration.K.tolist()
    data['D'] = incrementalCalibration.D.tolist()
    with open(calibrationFile, "w") as f:
        json.dump(data, f, indent=4)


def readEyeFishCalibration():
    with open(calibrationFile, "r") as f:
        data = json.load(f)
        K = np.array(data["K"])
        D = np.array(data["D"])

    return K,D



def writeLaneLimits(leftOrRight, realtimeLaneDetection):
    data = {}
    if leftOrRight == 'left':
        data['leftLine'] = realtimeLaneDetection.lanesLines[0].toList();
        fileName = leftLineFile
    else:
        data['rightLine'] = realtimeLaneDetection.lanesLines[1].toList();
        fileName = rightLineFile

    with open(fileName, "w") as f:
        json.dump(data, f, indent=4)



def readLaneLimits():
    with open(leftLineFile, "r") as f:
        data = json.load(f)
        leftLine = data['leftLine']

    with open(rightLineFile, "r") as f:
        data = json.load(f)
        rightLine = data['rightLine']

    return leftLine, rightLine

