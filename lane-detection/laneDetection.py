import matplotlib.pyplot as plt
import cv2
import numpy as np
from helper import *

class LaneDetector:
    def __init__(self, rho=6, theta=np.pi/60, threshold=160):
        self.rho = rho
        self.theta = theta
        self.threshold = threshold
        self.min_line_len = 40
        self.max_line_gap = 25


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
            for x1, y1, x2, y2 in line:
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
        if not right_line_y or not right_line_x or not left_line_y or not left_line_x:
            return None

        min_y = int(image.shape[0] * (3 / 5)) # <-- Just below the horizon
        max_y = image.shape[0] # <-- The bottom of the image
        poly_left = np.poly1d(np.polyfit(
            left_line_y,
            left_line_x,
            deg=1
        ))
        left_x_start = int(poly_left(max_y))
        left_x_end = int(poly_left(min_y))
        poly_right = np.poly1d(np.polyfit(
            right_line_y,
            right_line_x,
            deg=1
        ))
        right_x_start = int(poly_right(max_y))
        right_x_end = int(poly_right(min_y))

        return [[ [left_x_start, max_y, left_x_end, min_y],
                  [right_x_start, max_y, right_x_end, min_y], ]]

