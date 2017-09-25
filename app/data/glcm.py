from __future__ import division

import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from skimage.feature import greycomatrix, greycoprops
from sklearn.feature_extraction import image

SAMPLE_SIZE = 50

# def plototsu(img, title, subplot1, subplot2):
def plototsu(img):
        # plt.subplot(subplot1)
        # plt.title(title)

        threshold = threshold_otsu(img)
        binary = img >= threshold

        return binary
        # plt.imshow(binary, cmap='gray')
        #
        # plt.subplot(subplot2)
        # plt.hist(binary.ravel())
        # plt.title(title)


Pdry = cv2.imread('sandpaper-60-grit-red-filter/135.png', 0)
Pwet = cv2.imread('sandpaper-brown-60-grit/135.png', 0)

# Pdry = plototsu(Pdryraw)
# Pwet = plototsu(Pwetraw)

print "Pdy: ", Pdry


Pdry_samples = [ (40,30), (55,45), (80,20), (90,110), (75,75), (100,100), (50,300), (50, 360), (65, 299) ]
Pwet_samples = [ (40,30), (55,45), (80,20), (90,110), (75,75), (100,100), (50,300), (50, 360), (65, 299) ]

Pdry_patches = []

for loc in Pdry_samples:
    Pdry_patches.append(Pdry[loc[0]:loc[0] + SAMPLE_SIZE, loc[1]:loc[1] + SAMPLE_SIZE])

Pwet_patches = []

for loc in Pwet_samples:
    Pwet_patches.append(Pwet[loc[0]:loc[0] + SAMPLE_SIZE, loc[1]:loc[1] + SAMPLE_SIZE])

# Pdry_patches = image.extract_patches_2d(Pdry, (50, 50), 250)
# Pwet_patches = image.extract_patches_2d(Pwet, (50, 50), 250)

print "Pdry_patches: ", Pdry_patches
print "Pwet_patches: ", Pwet_patches

xs = []
ys = []

for patch in (Pdry_patches + Pwet_patches):
    try:
        glcm = greycomatrix(patch, [5], [0], 256, symmetric=True, normed=True)
        xs.append(greycoprops(glcm, 'dissimilarity')[0, 0])
        ys.append(greycoprops(glcm, 'correlation')[0, 0])
    except ValueError:
        pass

print "xs: ", xs
print "ys: ", ys

plt.scatter(xs, ys)
plt.show()

###########
# create the figure

# display original image with locations of patches

# for each patch, plot (dissimilarity, correlation)
fig, ax = plt.subplots()
ax.plot(xs[:len(Pdry_patches)], ys[:len(Pdry_patches)], 'go',
        label='Dry')
ax.plot(xs[len(Pwet_patches):], ys[len(Pwet_patches):], 'bx',
        label='Wet')
ax.set_xlabel('GLCM Dissimilarity')
ax.set_ylabel('GLCM Correlation')
ax.legend()




# display the patches and plot
fig.suptitle('Grey level co-occurrence matrix features', fontsize=14)
plt.show()



fig = plt.figure(figsize=(8, 6))
# axis = fig.add_subplot(3, 3, 3)
# display the image patches
for i, patch in enumerate(Pdry_patches):
    axis = fig.add_subplot(3, len(Pdry_patches), len(Pdry_patches)*1 + i + 1)
    axis.imshow(patch, cmap=plt.cm.gray, interpolation='nearest',
              vmin=0, vmax=255)
    axis.set_xlabel('Dry %d' % (i + 1))

for i, patch in enumerate(Pwet_patches):
    axis = fig.add_subplot(3, len(Pwet_patches), len(Pwet_patches)*2 + i + 1)
    axis.imshow(patch, cmap=plt.cm.gray, interpolation='nearest',
              vmin=0, vmax=255)
    axis.set_xlabel('Wet %d' % (i + 1))

###########

# plototsu(Pdry, 'dry', 221, 222)
# plototsu(Pwet, 'wet', 223, 224)

plt.show()
