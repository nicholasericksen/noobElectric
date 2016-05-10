#import numpy as np
#import matplotlib.pyplot as plt
#import Image

#from skimage import io
#from skimage import color

#img = io.imread('imgs/10cm.png')

#image = Image.open('imgs/10cm.png')
#image.show
#print(img)
#img = color.rgb2gray(img)
#bins = range(0, 256, 10)

#bin_counts, bin_edges, patches = plt.hist(img.ravel())

#plt.show()



import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

from skimage.filters import threshold_otsu

imgs = ['imgs/10cm.jpg', 'imgs/20cm.png']






img = mpimg.imread('imgs/10cm.jpg')

plt.imshow(img)
plt.title('10cm Tumor Depth', fontsize=18)
plt.xlabel('X-Coordinates', fontsize=14)
plt.ylabel('Y-Coordinates', fontsize=14)
plt.show()

plt.hist(img.ravel(), bins=256)
plt.title('10cm Tumor Histogram', fontsize=18)
plt.xlabel('Pixel Intensity', fontsize=14)
plt.ylabel('Frequency')

plt.show()

threshold = threshold_otsu(img)
print("threshold: ", threshold)
binary = img >= threshold

plt.imshow(binary)
plt.title('10cm Otsu Processed Tumor', fontsize=18)
plt.xlabel('X-Coordinate')
plt.ylabel('Y-Coordinate')
plt.show()

plt.hist(binary.ravel())
plt.title('10cm Otsu Processed Histogram', fontsize=18)
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.show()
