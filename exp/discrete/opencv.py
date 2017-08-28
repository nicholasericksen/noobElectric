from __future__ import division

import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from scipy.stats import norm
from skimage.filters import threshold_otsu

def plothist(img, title, subplot):
#        weights = np.ones_like(img)/float(len(img))

        plt.subplot(subplot)
        plt.hist(img.ravel(), normed=True)
        plt.xlabel('Grayscale Values')
        plt.ylabel('Frequency of Occurance')
        plt.title(title)


def plotimg(img, title, subplot):
        plt.subplot(subplot)
        plt.imshow(img, cmap='gray')
        plt.title(title)

def plototsu(img, title, subplot1, subplot2):
        plt.subplot(subplot1)
        plt.title(title)

        threshold = threshold_otsu(img)
        binary = img >= threshold

        plt.imshow(binary, cmap='gray')

        plt.subplot(subplot2)
        plt.hist(binary.ravel())
        plt.title(title)

#Read in the images
Hdryrawo = cv2.imread('polarizance/exp-05-02-17-type1/1wk-H.jpg', 0)
Vdryrawo = cv2.imread('polarizance/exp-05-02-17-type1/1wk-V.jpg', 0)
Pdryrawo = cv2.imread('polarizance/exp-05-02-17-type1/1wk-P.jpg', 0)
Mdryrawo = cv2.imread('polarizance/exp-05-02-17-type1/1wk-M.jpg', 0)

Hwetrawo = cv2.imread('polarizance/exp-05-02-17-type1/new-H.jpg', 0)
Vwetrawo = cv2.imread('polarizance/exp-05-02-17-type1/new-V.jpg', 0)
Pwetrawo = cv2.imread('polarizance/exp-05-02-17-type1/new-P.jpg', 0)
Mwetrawo = cv2.imread('polarizance/exp-05-02-17-type1/new-M.jpg', 0)


# S0dryrawo = cv2.imread('S0-dry.jpg', 0)
# S0wetrawo = cv2.imread('S0-wet.jpg', 0)

Hdryraw = np.array(Hdryrawo, dtype=np.float32)
Vdryraw = np.array(Vdryrawo, dtype=np.float32)
Pdryraw = np.array(Pdryrawo, dtype=np.float32)
Mdryraw = np.array(Mdryrawo, dtype=np.float32)

Hwetraw = np.array(Hwetrawo, dtype=np.float32)
Vwetraw = np.array(Vwetrawo, dtype=np.float32)
Pwetraw = np.array(Pwetrawo, dtype=np.float32)
Mwetraw = np.array(Mwetrawo, dtype=np.float32)
# S0dryraw = np.array(S0dryrawo, dtype=np.float32)
# S0wetraw = np.array(S0wetrawo, dtype=np.float32)

#TODO imlement better edge detection

Hdry = Hdryraw[200:400, 200:400]
Vdry = Vdryraw[200:400, 200:400]
Pdry = Pdryraw[200:400, 200:400]
Mdry = Mdryraw[200:400, 200:400]

Hwet = Hwetraw[200:400, 200:400]
Vwet = Vwetraw[200:400, 200:400]
Pwet = Pwetraw[200:400, 200:400]
Mwet = Mwetraw[200:400, 200:400]

# S0dry = S0dryraw[200:400, 200:400]
# S0wet = S0wetraw[200:400, 200:400]

S0dry = Hdry + Vdry
S0wet = Hwet + Vwet

S1dry = (Hdry - Vdry) / S0dry
S1wet = (Hwet - Vwet) / S0wet

S0Pwet = Pwet + Mwet
S0Pdry = Pdry + Mdry
S2wet = (Pwet - Mwet) / S0Pwet
S2dry = (Pdry - Mdry) / S0Pdry

print S2wet

X1 = S1dry.flatten()
Y1 = S2dry.flatten()

X2 = S1wet.flatten()
Y2 = S2wet.flatten()

(muS1dry, sigmaS1dry) = norm.fit(X1)
(muS2dry, sigmaS2dry) = norm.fit(Y1)

(muS1wet, sigmaS1wet) = norm.fit(X2)
(muS2wet, sigmaS2wet) = norm.fit(Y2)

print 'mu and sigma for S1 Dry', muS1dry , sigmaS1dry
print 'mu and sigma for S2 Dry', muS2dry, sigmaS2dry

print 'mu and sigma for S1 Wet', muS1wet, sigmaS1wet
print 'mu and sigma for S2 Wet', muS2wet , sigmaS2wet

plt.scatter(X1, Y1, marker='x', color='r', label='Dry Leaf')
plt.scatter(X2, Y2, marker='o', color='b', label='Wet Leaf')

plt.title('Stokes Parameters')
plt.xlabel('S1')
plt.ylabel('S2')
plt.legend(loc=0)
plt.show()

# # Plot S1 for dry and wet
# plt.hist(S1wet.ravel(), normed=True, label='S1 Wet')
# plt.hist(S1dry.ravel(), normed=True, label='S1 Dry')
#
# plt.title('S1 for Dry and Wet Leaves')
# plt.xlabel('S1 Values')
# plt.ylabel('Normalized Frequency')
# plt.legend(loc=0)
# plt.show()
#
# plt.hist(S2wet.ravel(), normed=True, label='S2 Wet')
# plt.hist(S2dry.ravel(), normed=True, label='S2 Dry')
#
# plt.title('S2 for Dry and Wet Leaves')
# plt.xlabel('S2 Values')
# plt.ylabel('Normalized Frequency')
# plt.legend(loc=0)
# plt.show()
#
#
# #Plot S1 dry leave components
# plotimg(Hdry, 'H dry', 231)
# plotimg(Vdry, 'Vdry', 232)
# plotimg(S1dry, 'S1 Dry', 233)
#
# plothist(Hdry, 'H Dry Histogram', 234)
# plothist(Vdry, 'V Dry Histogram', 235)
# plothist(S1dry, 'S1 Dry Histogram', 236)
#
# plt.show()
#
# #Plot S1 wet leaf components
# plotimg(Hwet, 'H wet', 231)
# plotimg(Vwet, ' V wet', 232)
# plotimg(S1wet, 'S1 wet', 233)
#
# plothist(Hwet, 'H wet', 234)
# plothist(Vwet, 'V wet', 235)
# plothist(S1wet, 'S1 wet', 236)
#
# plt.show()
#
# #Plot S2 dry leaf components
# plotimg(Hdry, 'P dry', 231)
# plotimg(Vdry, 'M dry', 232)
# plotimg(S2dry, 'S2 dry', 233)
#
# plothist(Pdry, 'P Dry', 234)
# plothist(Mdry, 'M Dry', 235)
# plothist(S2dry, 'S2 Dry', 236)
#
# plt.show()
#
# #Plot S2 wet leaf components
# plotimg(Pwet, 'P wet', 231)
# plotimg(Mwet, ' M wet', 232)
# plotimg(S2wet, 'S2 wet', 233)
#
# plothist(Pwet, 'P wet', 234)
# plothist(Mwet, 'M wet', 235)
# plothist(S2wet, 'S2 wet', 236)
#
# plt.show()
#
#
# #Plot hist of H and V
# #TODO include P and M.
# plt.hist(Hwet.ravel(), normed=True, facecolor='green', label='H wet')
# plt.hist(Vwet.ravel(), normed=True, facecolor='blue', label='V wet')
#
# plt.hist(Hdry.ravel(), normed=True, facecolor='black', label='H dry')
# plt.hist(Vdry.ravel(), normed=True, facecolor='red', label='V dry')
#
# plt.title("H, V Wet and Dry")
# plt.legend(loc=0)
# plt.show()
#
# plt.hist(Pwet.ravel(), normed=True, facecolor='green', label='P wet')
# plt.hist(Mwet.ravel(), normed=True, facecolor='blue', label='M wet')
#
# plt.hist(Pdry.ravel(), normed=True, facecolor='black', label='P dry')
# plt.hist(Mdry.ravel(), normed=True, facecolor='red', label='M dry')
#
# plt.title("P, M Wet and Dry")
# plt.legend(loc=0)
# plt.show()
#
# #plot S1
# plotimg(S1dry, "S1 Dry", 221)
# plotimg(S1wet, "S1 Wet", 222)
# plothist(S1dry, "S1 Dry Hist", 223)
# plothist(S1wet, "S1 Wet Hist", 224)
# plt.suptitle('S1 Analysis', fontsize=18)
# plt.show()
#
# #plot S2
# plotimg(S2dry, "S2 Dry", 221)
# plotimg(S2wet, "S2 Wet", 222)
# plothist(S2dry, "S2 Dry Hist", 223)
# plothist(S2wet, "S2 Wet Hist", 224)
# plt.suptitle("S2 Analysis", fontsize=18)
# plt.show()
#
# #Plot Otsu
# plototsu(S1wet, "S1 Wet Otsu", 221, 223)
# plototsu(S1dry, "S1 Dry Otsu", 222, 224)
#
# plt.show()
#
# plototsu(S2wet, "S2 Wet Otsu", 221, 223)
# plototsu(S2dry, "S2 Dry Otsu", 222, 224)
#
# plt.show()

# Calculate the DOLP
# DOLPdry = np.sqrt((np.square(S1dry)) + (np.square(S2dry))) / S0dry
# plt.hist(DOLPdry, bins=100)
# plt.title("DOLP of Dry Leaf")
# plt.show()
#
#
# DOLPwet = np.sqrt((np.square(S1wet)) + (np.square(S2wet))) / S0wet
# plt.title("DOLP of Wet Leaf")
# plt.hist(DOLPwet, bins=100)
#
# plt.show()
