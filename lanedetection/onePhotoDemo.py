import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from laneDetection import LaneDetector


# reading in an image
image = mpimg.imread(str(sys.argv[1]))


# TODO REMOVE:
# printing out some stats and plotting the image

print('This image is:', type(image), 'with dimensions:', image.shape)
laneDetector = LaneDetector(theta=np.pi/160, threshold=80)

laneLines = laneDetector.calculateLines(image)
print(laneLines[1])
plt.imshow(laneLines[0])
plt.show()
