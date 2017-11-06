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
# from flask import jsonify
# Connect to mongodb
client = MongoClient()
db = client.experiments

# np.seterr(divide='ignore', invalid='ignore')

# set numpy formatter to 2 decimal places
float_formatter = lambda x: "%.2f" % x
np.set_printoptions(formatter={'float_kind':float_formatter})

np.errstate(divide='ignore', invalid='ignore')
old_err_state = np.seterr(divide='raise')
ignored_states = np.seterr(**old_err_state)
#set the directory the images come from
EXPERIMENT_DIR = 'red-oak-4-white-diffuse-0wk/'

#Read the images for discrete analysis and flatten them
Hraw = np.array(cv2.imread(EXPERIMENT_DIR + 'H.png', 0), dtype=np.float32)
Vraw = np.array(cv2.imread(EXPERIMENT_DIR + 'V.png', 0), dtype=np.float32)
Praw = np.array(cv2.imread(EXPERIMENT_DIR + 'P.png', 0), dtype=np.float32)
Mraw = np.array(cv2.imread(EXPERIMENT_DIR + 'M.png', 0), dtype=np.float32)




SAMPLE_SIZE = 500


# Pdry = cv2.imread('sandpaper-brown-60-grit/90.png', 0)
# Pwet = cv2.imread('sandpaper-100-grit-brown-red-filter/90.png', 0)

Hpatches = image.extract_patches_2d(Hraw, (150, 150), SAMPLE_SIZE, 1)
Ppatches = image.extract_patches_2d(Praw, (150, 150), SAMPLE_SIZE, 1)
Vpatches = image.extract_patches_2d(Vraw, (150, 150), SAMPLE_SIZE, 1)
Mpatches = image.extract_patches_2d(Mraw, (150, 150), SAMPLE_SIZE, 1)

# Pwet_patches = image.extract_patches_2d(Praw, (50, 50), SAMPLE_SIZE, 1)

xs = []
ys = []

dataset = []
# xsWet = []
# ysWet = []
directory = EXPERIMENT_DIR + 'samples/'

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

def divide( a, b ):
    """ ignore / 0, div0( [-1, 0, 1], 0 ) -> [0, 0, 0] """
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.true_divide( a, b )
        c[ ~ np.isfinite( c )] = 0  # -inf inf NaN
    return c


for index, Ppatch in enumerate(Ppatches):
    filenameP = directory + 'P-sample-' + str(index) + '.png'
    cv2.imwrite(filenameP, Ppatches[index])
for index, Mpatch in enumerate(Mpatches):
    filenameM = directory + 'M-sample-' + str(index) + '.png'
    cv2.imwrite(filenameM, Mpatches[index])

for index, Vpatch in enumerate(Vpatches):
    filenameV = directory + 'V-sample-' + str(index) + '.png'
    cv2.imwrite(filenameV, Vpatches[index])


for index, Hpatch in enumerate(Vpatches):
    try:
        glcm = greycomatrix(Hpatch, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4], 256, symmetric=True, normed=True)
        dissimilarity = greycoprops(glcm, 'dissimilarity')[0, 0]
        correlation = greycoprops(glcm, 'correlation')[0, 0]

        xs.append(dissimilarity)
        ys.append(correlation)



        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = directory + 'H-sample-' + str(index) + '.png'
        cv2.imwrite(filename, Hpatches[index])

        H = Hpatches[index].ravel()
        V = Vpatches[index].ravel()
        P = Ppatches[index].ravel()
        M = Mpatches[index].ravel()

        # try:
        S1 = divide((H - V), 255.0)
        # except:
        # S1 = [0]
        # try:
        # print 'S1', S1
        S2 = divide((P - M), 255.0)
        # print 'S2', S2
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
        sample = {"file": filename, "dissimilarity": dissimilarity, "correlation": correlation, "S1": S1obj, "S2": S2obj}
        dataset.append(sample)
        # plt.scatter(S1, S2)
        # plt.show()
    except ValueError:
        print "ERROR"
        pass
# print "DATASET", dataset
# jsonData = jsonify({"data": dataset})

# print dataset
# result = db.glcm.insert(
#     {
#             'meta_id': ObjectId('59d28946b42de0dc534fabbc'),
#             'glcm': str(dataset)
#     }
# )


fig, ax = plt.subplots()
ax.plot(xs[:len(Hpatches)], ys[:len(Hpatches)], 'go',
        label='Dry')
# ax.plot(xsWet[:len(Pwet_patches)], ysWet[:len(Pwet_patches)], 'rx',
#         label='Wet')


ax.set_xlabel('GLCM Dissimilarity')
ax.set_ylabel('GLCM Correlation')
ax.legend()




# display the patches and plot
# fig.suptitle('Grey level co-occurrence matrix features', fontsize=14)
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

# fig = plt.figure(figsize=(8, 6))
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

plt.show()
