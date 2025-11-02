import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from laneDetection import LaneDetector


# reading in an image
image = mpimg.imread('roadPicture.jpg')


# TODO REMOVE:
# printing out some stats and plotting the image

plt.imshow(image)
plt.show()

print('This image is:', type(image), 'with dimensions:', image.shape)
laneDetector = LaneDetector()

laneLines = laneDetector.calculateLines(image)
print(laneLines)
