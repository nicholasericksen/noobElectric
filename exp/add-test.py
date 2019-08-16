import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import numpy as np

#Read in the images
img1 = mpimg.imread(str('H-dry.jpg'))
img2 = mpimg.imread(str('V-dry.jpg'))

def rgb2gray(rgb):
        return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

H = rgb2gray(img1)
V = rgb2gray(img2)

total = H + V

#h = np.ndarray(H, 'int8')
#print h
#Plot the images and results
plt.imshow(total, cmap = plt.get_cmap('gray'))
plt.imshow(V, cmap = plt.get_cmap('gray'))

plt.show()
