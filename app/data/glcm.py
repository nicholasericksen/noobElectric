from __future__ import division

import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from skimage.feature import greycomatrix, greycoprops
from sklearn.feature_extraction import image
from scipy.stats import gaussian_kde
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
# Connect to mongodb
client = MongoClient()
db = client.experiments

# np.seterr(divide='ignore', invalid='ignore')

# set numpy formatter to 2 decimal places
float_formatter = lambda x: "%.2f" % x
np.set_printoptions(formatter={'float_kind':float_formatter})
# np.errstate(divide='ignore', invalid='ignore')
old_err_state = np.seterr(divide='raise')
ignored_states = np.seterr(**old_err_state)
#set the directory the images come from
imagedirectory = 'test/'

#Read the images for discrete analysis and flatten them
Hraw = np.array(cv2.imread(imagedirectory + 'H.png', 0), dtype=np.int)
Vraw = np.array(cv2.imread(imagedirectory + 'V.png', 0), dtype=np.int)
Praw = np.array(cv2.imread(imagedirectory + 'P.png', 0), dtype=np.int)
Mraw = np.array(cv2.imread(imagedirectory + 'M.png', 0), dtype=np.int)




SAMPLE_SIZE = 5

EXPERIMENT_DIR = 'test/'

# Pdry = cv2.imread('sandpaper-brown-60-grit/90.png', 0)
# Pwet = cv2.imread('sandpaper-100-grit-brown-red-filter/90.png', 0)

Hpatches = image.extract_patches_2d(Hraw, (50, 50), SAMPLE_SIZE, 1)
Ppatches = image.extract_patches_2d(Praw, (50, 50), SAMPLE_SIZE, 1)
Vpatches = image.extract_patches_2d(Vraw, (50, 50), SAMPLE_SIZE, 1)
Mpatches = image.extract_patches_2d(Mraw, (50, 50), SAMPLE_SIZE, 1)

# Pwet_patches = image.extract_patches_2d(Praw, (50, 50), SAMPLE_SIZE, 1)

xs = []
ys = []

dataset = []
# xsWet = []
# ysWet = []

def datasummary(data):
    maxValue = np.amax(data)
    minValue = np.amin(data)
    length = len(data)
    mean = np.mean(data)
    std = np.std(data)

    return {
        "max": maxValue,
        "min": minValue,
        "mean": mean,
        "std": std,
        "numpts": length
    }

def createhistogram(data, bins):
    hist = np.histogram(data, bins=bins)
    bins = hist[1].tolist()
    values = hist[0].tolist()

    # Convert the tuples into arrays for smaller formatting
    zipped = [list(t) for t in zip(bins, values)]
    # print "zipped", zipped

    return zipped

for index, Hpatch in enumerate(Hpatches):
    try:
        glcm = greycomatrix(Hpatch, [5], [0], 256, symmetric=True, normed=True)
        dissimilarity = greycoprops(glcm, 'dissimilarity')[0, 0]
        correlation = greycoprops(glcm, 'correlation')[0, 0]

        xs.append(dissimilarity)
        ys.append(correlation)

        directory = EXPERIMENT_DIR + 'samples/H'

        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = directory + 'H-sample-' + str(index) + '.png'
        cv2.imwrite(filename, Hpatches[index])

        H = Hpatches[index].ravel()
        V = Vpatches[index].ravel()
        P = Ppatches[index].ravel()
        M = Mpatches[index].ravel()

        # try:
        S1 = np.divide((H - V), (H + V))
        # except:
        # S1 = [0]
        # try:
        S2 = np.divide((P - M), (P + M))
        # except:
        # S2 = [0]
        # Print statistics about Stokes data
        S1summary = datasummary(S1)
        S2summary = datasummary(S2)

        # Create the S1 and S2 Histogram
        S1zipped = createhistogram(S1, np.arange(-1, 1.01, 0.01))
        S2zipped = createhistogram(S2, np.arange(-1, 1.01, 0.01))

        S1obj = {
            "data": S1zipped,
            "stats": S1summary
        }

        S2obj = {
            "data": S2zipped,
            "stats": S1summary
        }
        S = [list(t) for t in zip(S1, S2)]

        #['filename', xs, ys, [S1], [S2], [[patch]]]
        sample = {"file": filename, "dissimilarity": dissimilarity, "correlation": correlation, "S1": S1obj, "S2": S2obj, "S": S}
        dataset.append(sample)
        # plt.scatter(S1, S2)
        # plt.show()
    except ValueError:
        print "ERROR"
        pass
print "DATASET", dataset

# print dataset
result = db.discrete.update(
    {
        '_id': ObjectId('59b86c8bb42de0886d65ccbc')
    },
    {
        '$set': {
            "glcm": dataset
        }
    }
)


fig, ax = plt.subplots()
ax.plot(xs[:len(Hpatches)], ys[:len(Hpatches)], 'go',
        label='Dry')
# ax.plot(xsWet[:len(Pwet_patches)], ysWet[:len(Pwet_patches)], 'rx',
#         label='Wet')
ax.set_xlabel('GLCM Dissimilarity')
ax.set_ylabel('GLCM Correlation')
ax.legend()




# display the patches and plot
fig.suptitle('Grey level co-occurrence matrix features', fontsize=14)
# plt.show()
# for patch in patches:
#     try:
#         glcm = greycomatrix(patch, [5], [0], 256, symmetric=True, normed=True)
#         xsDry.append(greycoprops(glcm, 'dissimilarity')[0, 0])
#         ysDry.append(greycoprops(glcm, 'correlation')[0, 0])
#     except ValueError:
#         pass


###########
# create the figure

# display original image with locations of patches

# for each patch, plot (dissimilarity, correlation)


# print "Pdry[0]", Hpatches[0]

fig = plt.figure(figsize=(8, 6))
# axis = fig.add_subplot(3, 3, 3)
# display the image patches
# for i, patch in enumerate(patches):
#     while (i <= 5):
#         axis = fig.add_subplot(3, len(patches), len(patches)*1 + i + 1)
#         axis.imshow(patch, cmap=plt.cm.gray, interpolation='nearest',
#               vmin=0, vmax=255)
#         axis.set_xlabel('Dry %d' % (i + 1))
#
# for i, patch in enumerate(Pwet_patches):
#     while(i <= 5):
#
#         axis = fig.add_subplot(3, len(Pwet_patches), len(Pwet_patches)*2 + i + 1)
#         axis.imshow(patch, cmap=plt.cm.gray, interpolation='nearest',
#               vmin=0, vmax=255)
#         axis.set_xlabel('Wet %d' % (i + 1))

###########
# i = 0
# while (i < len(patches)):
#     # filename = 'p-dry-sample-' + str(i) + '.png'
#     # cv2.imwrite('./test/' + filename, patches[i])
#     i = i + 1

# plt.show()
