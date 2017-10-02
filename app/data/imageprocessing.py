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
imagedirectory = 'exp-07-13-17-basil/'
# sampledirectroy = os.path.join()

#Read the images for discrete analysis and flatten them
Hraw = np.array(cv2.imread(imagedirectory + 'H.png', 0).ravel(), dtype=np.int)
Vraw = np.array(cv2.imread(imagedirectory + 'V.png', 0).ravel(), dtype=np.int)
Praw = np.array(cv2.imread(imagedirectory + 'P.png', 0).ravel(), dtype=np.int)
Mraw = np.array(cv2.imread(imagedirectory + 'M.png', 0).ravel(), dtype=np.int)

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
# plt.scatter(S1, S2)
# plt.show()

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
    print "zipped", zipped

    return zipped

# Print statistics about Stokes data
S1summary = datasummary(S1)
S2summary = datasummary(S2)

# Create the S1 and S2 Histogram
S1zipped = createhistogram(S1, np.arange(-1, 1.01, 0.01))
S2zipped = createhistogram(S2, np.arange(-1, 1.01, 0.01))

# Create measurement Histograms
Hzipped = createhistogram(H, np.arange(0, 256, 1))
Vzipped = createhistogram(V, np.arange(0, 256, 1))
Pzipped = createhistogram(P, np.arange(0, 256, 1))
Mzipped = createhistogram(M, np.arange(0, 256, 1))

result = db.discrete.insert_one(
    {
        "title": "Basil a La Mode",
        "summary": "This is an LMP based polarizance setup with images taken of a basil plant",
        "description": "The purpose of this experiment was to examine the surface polarization characteristics of a basil leaf.  An unpolarized source was utilized, in conjuction with a linear polarizer, to generate incident rays of light onto the leafs' surface.  The resulting polarization intensities were measured at 0, 90, 45, and 135 degrees and the Polarizance vector of the Mueller matrice was determined.",
        "date": str(datetime.utcnow()),
        "images": 'exp-07-13-17-basil',
        "histograms": {
            "measurements": {
                "H": Hzipped,
                "V": Vzipped,
                "P": Pzipped,
                "M": Mzipped
            },
            "stokes": {
                "S1": {
                    "data": S1zipped,
                    "stats": S1summary
                },
                "S2": {
                    "data": S2zipped,
                    "stats": S2summary
                }
            }
        }
    }
)
