import cv2
import os
import sys
from datetime import datetime


class Recorder:
    """
        Recorder object that saves in the specified folder
        following the pattern video_YYYYMMDD_hhmmss.mp4
        sequences of video of maximum defined size.
    """
    def __init__(self, maxSize, folder):
        self.maxSize = maxSize 
        self.folder = folder

        self.sized = False
        self.out = None
        self.fourcc = cv2.VideoWriter_fourcc(*'avc1')
        self.createFileName()



    def process(self, frame):
        """
            Callback for being invoked from Camera.process.
        """
        if self.sized:
            if os.path.getsize(self.outFile) > self.maxSize:
                self.out.release()
                self.createFileName()
                self.out = cv2.VideoWriter(self.outFile, self.fourcc, \
                        20.0, (self.width, self.height))

            self.out.write(frame)

        else:
            self.height, self.width = frame.shape[:2]
            self.sized = True
            self.out = cv2.VideoWriter(self.outFile, self.fourcc, 20.0, \
                    (self.width, self.height))
            if not self.out.isOpened():
                raise "ERROR: VideoWriter failed to open file " + self.outFile



    def createFileName(self):
        """
            Private method.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fileName = f"FILE_{timestamp}.mp4"
        self.outFile = os.path.join(self.folder, fileName)
        print("Writting to file " + self.outFile)



    def __del__(self):
        if self.out != None: self.out.release()
        self.outFile = None
        self.sized = False
