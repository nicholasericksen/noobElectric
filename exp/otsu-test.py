import matplotlib.pyplot as plt
import numpy as np
from numpy import random

from skimage.filters import threshold_otsu

test = random.random((3,3))
print "Test Pattern"
print test

#Plot the random test image
plt.subplot(221)
plt.title("Random Grayscale Image")
plt.axis("off")
plt.imshow(test, cmap='gray', interpolation='nearest')


#Plot the random histogram
plt.subplot(222)
plt.title("Random Image Histogram")
plt.hist(test.ravel(), normed=True)

#Calculate the Otsu threshold
threshold = threshold_otsu(test)
print "Threshold: ", threshold

binary = test >= threshold
print "Binary: "
print binary

#Plot the Binary image
plt.subplot(223)
plt.title("Binary Image")
plt.axis("off")
plt.imshow(binary, cmap='gray', interpolation='nearest')

#Plot the Binary Histogram
plt.subplot(224)
plt.title("Binary Image Histogram")
plt.hist(binary.ravel(), normed=True)

plt.suptitle("Otsu Thresholding Example", fontsize=18)
plt.show()

