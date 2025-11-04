import matplotlib.pyplot as plt
import cv2
import numpy as np
from helper import *

class LaneDetector:
    def __init__(self, rho=6, theta=np.pi/60, threshold=160, min_line_len=40, max_line_gap=25):
        self.rho = rho
        self.theta = theta
        self.threshold = threshold
        self.min_line_len = min_line_len
        self.max_line_gap = max_line_gap
        self.previousLaneLines = None
        self.inertia = 10
        


    def calculateLines(self, img):
        # Detect edges : Canny Transformation
        cannyed_image = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), 100, 200)
        #plt.imshow(cannyed_image)
        #plt.show()


        # Define region of interest
        cropped_image = self.regionOfInterest(cannyed_image)

        #plt.imshow(cropped_image)
        #plt.show()


        # Line detection: Hough Transformation
        lines = cv2.HoughLinesP(cropped_image,
                rho=self.rho, theta=self.theta,
                threshold=self.threshold,
                lines=np.array([]), 
                minLineLength=self.min_line_len, maxLineGap=self.max_line_gap)


        # Right and left main lines detection
        laneLines = self.detectLaneLine(lines, img)
        if self.previousLaneLines:
            if not laneLines[0]: laneLines[0] = self.previousLaneLines[0]
            if not laneLines[1]: laneLines[1] = self.previousLaneLines[1]

        self.previousLaneLines = laneLines

        if not laneLines:
            return img, None

        line_image = self.drawLines(img, laneLines)
        #plt.imshow(line_image)
        #plt.show()

        return line_image, laneLines

    #
    # Crops to the area of interest: an isosceles triangle with the perspective of the
    # road lines.
    #
    def regionOfInterest(self, img):
        height = img.shape[0]
        width = img.shape[1]
        region_of_interest_vertices = [
            (0, height),
            (width / 2, height / 2),
            (width, height),
        ]

        mask = np.zeros_like(img)
        #match_mask_color = (255,) * img.shape[2]
        match_mask_color = 255
        cv2.fillPoly(mask, np.array([region_of_interest_vertices], np.int32), match_mask_color)
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image



    #
    # On the given image, draws the lines listed in the parameter
    #
    def drawLines(self, img, lines, color=[255, 0, 0], thickness=3):
        # If there are no lines to draw, exit.
        if lines is None:
            return
        # Create a blank image that matches the original in size.
        line_img = np.zeros(
            (img.shape[0], img.shape[1], img.shape[2]), dtype=np.uint8,)
        # Loop over all lines and draw them on the blank image.
        for line in lines:
            if not line: continue
            x1 = int(line[0])
            y1 = int(line[1])
            x2 = int(line[2])
            y2 = int(line[3])
            cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
        # Merge the image with the lines onto the original.
        img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)
        # Return the modified image.
        return img

 

    #
    # Detects main lane lines.
    # TODO: parametrize!!!
    #
    def detectLaneLine(self, lines, image):
        if lines is None: return None

        left_line_x = []
        left_line_y = []
        right_line_x = []
        right_line_y = []
        laneLines = [None, None]
        for line in lines:
            for x1, y1, x2, y2 in line:
                slope = (y2 - y1) / (x2 - x1) # <-- Calculating the slope.
                if math.fabs(slope) < 0.5: # <-- Only consider extreme slope
                 continue
                if slope <= 0: # <-- If the slope is negative, left group.
                    left_line_x.extend([x1, x2])
                    left_line_y.extend([y1, y2])
                else: # <-- Otherwise, right group.
                    right_line_x.extend([x1, x2])
                    right_line_y.extend([y1, y2])
        #if not right_line_y or not right_line_x or not left_line_y or not left_line_x:
        #    return None

        min_y = int(image.shape[0] * (3 / 5)) # <-- Just below the horizon
        max_y = image.shape[0] # <-- The bottom of the image

        if left_line_y and left_line_x:
            poly_left = np.poly1d(np.polyfit(
                left_line_y, left_line_x, deg=1))
            left_x_start = int(poly_left(max_y))
            left_x_end = int(poly_left(min_y))

            # Inertia of previous line
            if self.previousLaneLines and self.previousLaneLines[0]:
                left_x_start = (left_x_start + 
                    self.inertia*self.previousLaneLines[0][0])/(self.inertia+1)
                left_x_end = (left_x_end + 
                    self.inertia*self.previousLaneLines[0][2])/(self.inertia+1)

            laneLines[0] = [left_x_start, max_y, left_x_end, min_y]


        if right_line_y and right_line_x: 
            poly_right = np.poly1d(np.polyfit(
                right_line_y, right_line_x, deg=1))
            right_x_start = int(poly_right(max_y))
            right_x_end = int(poly_right(min_y))

            # Inertia of previous line
            if self.previousLaneLines and self.previousLaneLines[1]:
                right_x_start = (right_x_start + 
                    self.inertia * self.previousLaneLines[1][0])/(self.inertia+1)
                right_x_end = (right_x_end + 
                    self.inertia* self.previousLaneLines[1][2])/(self.inertia+1)

            laneLines[1] = [right_x_start, max_y, right_x_end, min_y]

        return laneLines

