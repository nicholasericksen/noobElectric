from __future__ import division
import numpy as np
import cv2
from pymongo import MongoClient
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from datetime import datetime

# Connect to mongodb
client = MongoClient()
db = client.experiments

# set numpy formatter to 2 decimal places
float_formatter = lambda x: "%.2f" % x
np.set_printoptions(formatter={'float_kind':float_formatter})

#set the directory the images come from
imagedirectory = 'exp-07-13-17-pepper/'

#Read the images for discrete analysis and flatten them
Hraw = np.array(cv2.imread(imagedirectory + '0.jpg', 0).ravel(), dtype=np.int)
Vraw = np.array(cv2.imread(imagedirectory + '90.jpg', 0).ravel(), dtype=np.int)
Praw = np.array(cv2.imread(imagedirectory + '45.jpg', 0).ravel(), dtype=np.int)
Mraw = np.array(cv2.imread(imagedirectory + '135.jpg', 0).ravel(), dtype=np.int)

zeroindex = []
index = 0
while (index < len(Hraw)):
    # Remove if all are 0 and/or Nan values
    if (Hraw[index] == 0 or np.isnan(Hraw[index])) and (Vraw[index] == 0 or np.isnan(Vraw[index])) or (Praw[index] == 0 or np.isnan(Praw[index])) and (Mraw[index] == 0 or np.isnan(Mraw[index])):
        zeroindex.append(index)
    index += 1

print 'Number of points removed: ', len(zeroindex)

# Remove values from all arrays equally so as to retain the size
H = np.delete(Hraw, zeroindex, axis=0)
V = np.delete(Vraw, zeroindex, axis=0)
P = np.delete(Praw, zeroindex, axis=0)
M = np.delete(Mraw, zeroindex, axis=0)

# Possible want this to be the normalizing factor
# S0 = cv2.imread(imagedirectory + 'clear.jpg', 0)

# Calculate the Stokes parameters
# Power intensities are taken and normalized
S1 = (H - V) / (H + V)
S2 = (P - M) / (P + M)

# Plot S1 S2 scatter Plot
# TODO remove this in favor of api usage
plt.scatter(S1, S2)
plt.show()

def datasummary(data):
    maxValue = np.amax(data)
    minValue = np.amin(data)
    length = len(data)

    #TODO Add median and mean and variance
    print '\n==========Summary==========='
    print 'max: ', maxValue
    print 'min: ', minValue
    print 'length: ', length
    print '============================\n'

    return {
        maxValue: maxValue,
        minValue: minValue,
        length: length
    }

def createhistogram(data, bins):
    hist = np.histogram(data, bins=bins)
    # rawbins = hist[1]
    # rawbins.round(decimals=2)
    bins = hist[1].tolist()
    values = hist[0].tolist()
    # values = [ '%.2f' % elem for elem in unformattedvalues ]

    # Convert the tuples into arrays for smaller formatting
    zipped = [list(t) for t in zip(bins, values)]
    print "zipped", zipped

    # Print Summary
    # print '\n==========Summary==========='
    # print 'histo: ', hist
    # print 'bins: ', bins
    # print 'values: ', values
    # print '==============================\n'

    return zipped

# Print statistics about Stokes data
datasummary(S1)
datasummary(S2)

# Create the S1 and S2 Histogram
S1zipped = createhistogram(S1, np.arange(-1, 1.01, 0.01))
S2zipped = createhistogram(S2, np.arange(-1, 1.01, 0.01))

# Create measurement Histograms
Hzipped = createhistogram(H, np.arange(0, 256, 1))
Vzipped = createhistogram(V, np.arange(0, 256, 1))
Pzipped = createhistogram(P, np.arange(0, 256, 1))
Mzipped = createhistogram(M, np.arange(0, 256, 1))

# plt.hist(S1)
# plt.show()
# plt.hist(S2)
#
# plt.show()

result = db.discrete.insert_one(
    {
        "title": "Le poivre et la lumiere",
        "description": "This is an LMP based polarizance setup with images taken of a pepper plant",
        "date": str(datetime.utcnow()),
        "images": '/data/exp-07-13-17-pepper/',
        "histograms": {
            "measurements": {
                "H": Hzipped,
                "V": Vzipped,
                "P": Pzipped,
                "M": Mzipped
            },
            "stokes": {
                "S1": S1zipped,
                "S2": S2zipped
            }
        }
    }
)
