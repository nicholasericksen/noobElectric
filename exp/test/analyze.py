from __future__ import division

import cv2
import random

import numpy as np
import matplotlib.pyplot as plt

from sklearn.feature_extraction import image
from sklearn import svm
from skimage.feature import greycomatrix, greycoprops

gHd,  rVd, Hdry = cv2.split(cv2.imread('exp-04-18-17-type1/1wk/0.jpg', 1))
gVd,  rVd, Vdry = cv2.split( cv2.imread('exp-04-18-17-type1/1wk/90.jpg', 1))
gPd,  rPd, Pdry = cv2.split( cv2.imread('exp-04-18-17-type1/1wk/45.jpg', 1))
gMd,  rMd, Mdry = cv2.split( cv2.imread('exp-04-18-17-type1/1wk/135.jpg', 1))

gHw, rHw, Hwet = cv2.split(cv2.imread('exp-04-18-17-type1/0wk/0.jpg', 1))
gVw, rVw, Vwet = cv2.split(cv2.imread('exp-04-18-17-type1/0wk/90.jpg', 1))
gPw, rPw, Pwet = cv2.split(cv2.imread('exp-04-18-17-type1/0wk/45.jpg', 1))
gMw, rMw, Mwet = cv2.split(cv2.imread('exp-04-18-17-type1/0wk/135.jpg', 1))

# Hdry = Hdry_raw[200:240, 250:290]
# Vdry = Vdry_raw[200:240, 250:290]
# Pdry = Pdry_raw[200:240, 250:290]
# Mdry = Mdry_raw[200:240, 250:290]
#
# Hwet = Hwet_raw[200:240, 250:290]
# Vwet = Vwet_raw[200:240, 250:290]
# Pwet = Pwet_raw[200:240, 250:290]
# Mwet = Mwet_raw[200:240, 250:290]
print "Hdry", Hdry

#Hdry = image.extract_patches_2d(Hdry_raw, (25,25), 500, 1)
#Vdry = image.extract_patches_2d(Vdry_raw, (25,25), 500, 1)
#Pdry = image.extract_patches_2d(Pdry_raw, (25,25), 500, 1)
#Mdry = image.extract_patches_2d(Mdry_raw, (25,25), 500, 1)

#Hwet = image.extract_patches_2d(Hwet_raw, (25,25), 500, 1)
#Vwet = image.extract_patches_2d(Vwet_raw, (25,25), 500, 1)
#Pwet = image.extract_patches_2d(Pwet_raw, (25,25), 500, 1)
#Mwet = image.extract_patches_2d(Mwet_raw, (25,25), 500, 1)
#Hdry_crop = Hdry[100:100, 100:100]
#Vdry_crop = Vdry[100:100, 100:100]

#for index, Hpatch in enumerate(Hwet):
#        tfd
# Calculate Stokes parameters
S1dry_raw = (Hdry - Vdry) / (Hdry + Vdry)
S1dry_raw[ ~ np.isfinite( S1dry_raw )] = 0

S2dry_raw = (Pdry - Mdry) / (Pdry + Mdry)
S2dry_raw[ ~ np.isfinite( S2dry_raw )] = 0

S1wet_raw = (Hwet - Vwet) / (Hwet + Vwet)
S1wet_raw[ ~ np.isfinite( S1wet_raw )] = 0

S2wet_raw = (Pwet - Mwet) / (Pwet + Mwet)
S2wet_raw[ ~ np.isfinite( S2wet_raw )] = 0

S1dry_ravel = np.ravel(S1dry_raw[200:290, 250:290])
S2dry_ravel = np.ravel(S2dry_raw[200:290, 250:290])
S1wet_ravel = np.ravel(S1wet_raw[200:290, 250:290])
S2wet_ravel = np.ravel(S2dry_raw[200:290, 250:290])
# Generate GLCM window
# xs_dry = []
# xs_wet = []
# ys_dry = []
# ys_wet = []

glcm_dry = greycomatrix(Hdry[200:290, 250: 290], [5], [0], 256, symmetric=True, normed=True)
dry_diss = greycoprops(glcm_dry, 'dissimilarity')[0, 0]
dry_corr = greycoprops(glcm_dry, 'correlation')[0, 0]

glcm_dry_corr_arr = np.empty(S1dry_ravel.size)
glcm_dry_corr_arr.fill(dry_corr)
glcm_dry_diss_arr = np.empty(S1dry_ravel.size)
glcm_dry_diss_arr.fill(dry_diss)

print "glcm_dry_corr_arr", glcm_dry_corr_arr

glcm_wet = greycomatrix(Hwet[200:290, 250: 290], [5], [0], 256, symmetric=True, normed=True)
wet_diss = greycoprops(glcm_wet, 'dissimilarity')[0, 0]
wet_corr = greycoprops(glcm_wet, 'correlation')[0, 0]

glcm_wet_corr_arr = np.empty(S1wet_ravel.size)
glcm_wet_diss_arr = np.empty(S1wet_ravel.size)
glcm_wet_corr_arr.fill(wet_corr)
glcm_wet_diss_arr.fill(wet_diss)
print "glcm_wet_corr_arr", glcm_wet_corr_arr
# Create data pt for each px
dry = np.dstack((S1dry_ravel, S2dry_ravel, glcm_dry_corr_arr, glcm_dry_diss_arr))
wet = np.dstack((S1wet_ravel, S2wet_ravel, glcm_wet_corr_arr, glcm_wet_diss_arr))
print "S1dry", dry
print "S1wet", wet

#S1dry = np.random.choice(dry_data, 500)
#S1wet = np.random.choice(wet_data, 500)

X = np.vstack((dry[0], wet[0]))

print "X", X

dry_class = np.empty(dry.size)
wet_class = np.empty(wet.size)

print "X.size", X.size
dry_class.fill(0)
wet_class.fill(1)

print "Dry", dry_class
print "Wet", wet_class

y = np.append(dry_class, wet_class)

print "y.size", y.size

# define the classifier
clf = svm.SVC()

fit = clf.fit(X.reshape(X.size, -1), y)

glcm_dry_test = greycomatrix(Hdry[300:390, 350: 390], [5], [0], 256, symmetric=True, normed=True)
dry_diss_test = greycoprops(glcm_dry_test, 'dissimilarity')[0, 0]
dry_corr_test = greycoprops(glcm_dry_test, 'correlation')[0, 0]

glcm_dry_corr_test = np.empty(S1dry_ravel.size)
glcm_dry_diss_test = np.empty(S1dry_ravel.size)
glcm_dry_corr_test.fill(dry_corr_test)
glcm_dry_diss_test.fill(dry_diss_test)


glcm_wet_test = greycomatrix(Hwet[300:390, 350: 390], [5], [0], 256, symmetric=True, normed=True)
wet_diss_test = greycoprops(glcm_wet_test, 'dissimilarity')[0, 0]
wet_corr_test = greycoprops(glcm_wet_test, 'correlation')[0, 0]

glcm_wet_corr_test = np.empty(S1wet_ravel.size)
glcm_wet_diss_test = np.empty(S1wet_ravel.size)
glcm_wet_corr_test.fill(wet_corr_test)
glcm_wet_diss_test.fill(wet_diss_test)
# fit = clf.fit(X, y)
dry_test = np.dstack((np.ravel(S1dry_raw[300:390, 350: 390]), np.ravel(S2dry_raw[300:390, 350: 390]), glcm_dry_corr_test, glcm_dry_diss_test))
wet_test = np.dstack((np.ravel(S1wet_raw[300:390, 350: 390]), np.ravel(S1dry_raw[300:390, 350: 390]), glcm_wet_corr_test, glcm_wet_diss_test))
dry_class_test = np.empty(dry_test.size)
wet_class_test = np.empty(wet_test.size)

dry_class_test.fill(0)
wet_class_test.fill(1)

X_test = np.append(dry_test, wet_test)
y_test = np.append(dry_class_test, wet_class_test)

score = fit.score(X_test.reshape(X_test.size,-1), y_test)

print "score: ", score
