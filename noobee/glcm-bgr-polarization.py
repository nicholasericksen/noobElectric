"""
This version does the glcm analysis on the stokes false images.
"""
from __future__ import division
import numpy as np
import os
import cv2
from sklearn.feature_extraction import image
import matplotlib.pyplot as plt
from skimage.feature import greycomatrix, greycoprops
# from .texture import extract_texture
def extract_texture(samples):
    # print "Hellow", samples
    """
    Generate GLCM based texture features for a given color channel.

    Args:
        samples (array): Array containing each image sample.  Each sample is a
            matrix of pixel intensities for a single color channel.
    Returns:
        array: Texture features extracted for an individual color channel.
    """
    texture = []
    for sample in samples:
        # print "smaple", sample.shape
        try:
            # Calculate texture features for a given sample
            relationships = [0, np.pi/4, np.pi/2, 3*np.pi/4]
            glcm = greycomatrix(sample, [1], relationships, 256, symmetric=True, normed=True)
            metrics = ['dissimilarity', 'contrast', 'correlation', 'energy']
            diss, contrast, corr, energy = [greycoprops(glcm, metric)[0, 0] for metric in metrics]

            texture.append([diss, contrast, corr, energy])
        except ValueError:
            print "Error in extracting the texture features"

    return np.array(texture)

def datasummary(raw_data):
    data = raw_data.ravel()
    maxValue = np.amax(data)
    minValue = np.amin(data)
    length = len(data)
    mean = np.mean(data)
    std = np.std(data)

    return np.array([mean, std])

def createhistogram(raw_data, bins):
    data = raw_data.ravel()
    # bins = np.arange(np.floor(data.min()),np.ceil(data.max()))
    hist = np.histogram(data, bins=bins)
    bins = bins.tolist()
    # / len(data) to normalize to 1
    values = hist[0] / len(data)

    # Convert the tuples into arrays for smaller formatting
    zipped = [list(t) for t in zip(bins, values.tolist())]

    return zipped

def calculate_stokes((P1, P2)):
    P1 = P1.astype(np.int16)
    P2 = P2.astype(np.int16)

    S = (P1 - P2) / (P1 + P2)

    # These represent values that have not been illuminated by the source
    # ie they are the product of masking and shadowing.
    S[~np.isfinite(S)] = 0

    return S

# Settings
img_dir = '../app/data/sandpaper-brown-60-grit'
size = 75
count = 100
# H = cv2.imread(os.path.join(img_dir, 'H.png'), 1)
# V = cv2.imread(os.path.join(img_dir, 'V.png'), 1)
# P = cv2.imread(os.path.join(img_dir, 'P.png'), 1)
# M = cv2.imread(os.path.join(img_dir, 'M.png'), 1)
H, V, P, M = [cv2.imread(os.path.join(img_dir, filter_angle), 1) for filter_angle in ['H.png', 'V.png', 'P.png', 'M.png']]
# print "H", H
S1, S2 = [calculate_stokes(filter_pair) for filter_pair in [(H,V), (P,M)]]
# print "S1", cv2.split(S1)
S1_b, S1_g, S1_r = cv2.split(S1)
S2_b, S2_g, S2_r = cv2.split(S2)


# cv2.imshow('sdf',S1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# extract samples from image
S1_b_samples, S1_g_samples, S1_r_samples = [image.extract_patches_2d(polarization, (size, size), count, 1) for polarization in [S1_b, S1_g, S1_r]]
S2_b_samples, S2_g_samples, S2_r_samples = [image.extract_patches_2d(polarization, (size, size), count, 1) for polarization in [S2_b, S2_g, S2_r]]

S1_b_summary = [datasummary(sample) for sample in S1_b_samples]
S1_g_summary = [datasummary(sample) for sample in S1_g_samples]
S1_r_summary = [datasummary(sample) for sample in S1_r_samples]

S2_b_summary = [datasummary(sample) for sample in S2_b_samples]
S2_g_summary = [datasummary(sample) for sample in S2_g_samples]
S2_r_summary = [datasummary(sample) for sample in S2_r_samples]
print S1_r_summary


S1_b_texture, S1_g_texture, S1_r_texture = [extract_texture(samples) for samples in [S1_b_samples.astype(np.uint8), S1_g_samples.astype(np.uint8), S1_r_samples.astype(np.uint8)]]
S2_b_texture, S2_g_texture, S2_r_texture = [extract_texture(samples) for samples in [S2_b_samples.astype(np.uint8), S2_g_samples.astype(np.uint8), S2_r_samples.astype(np.uint8)]]
# S1_b_texture = extract_texture(S1_r_samples.astype(np.uint8))
print np.concatenate((S1_r_summary, S1_r_texture), axis=1)
S1_b_features = np.concatenate((S1_b_summary, S1_b_texture), axis=1)
S1_g_features = np.concatenate((S1_g_summary, S1_g_texture), axis=1)
S1_r_features = np.concatenate((S1_r_summary, S1_r_texture), axis=1)

S2_b_features = np.concatenate((S2_b_summary, S2_b_texture), axis=1)
S2_g_features = np.concatenate((S2_g_summary, S2_g_texture), axis=1)
S2_r_features = np.concatenate((S2_r_summary, S2_r_texture), axis=1)

features = np.concatenate((S1_b_features, S1_g_features, S1_r_features, S2_b_features, S2_g_features, S2_r_features), axis=1)

# with open('sandpaper.csv', 'a') as f:
#     np.savetxt(f, features, delimiter=',', fmt="%g")


# print np.std(S1_r)
# plt.hist(createhistogram(S1_r, bins=np.linspace(-1,1,200)))
# plt.show()

# calculate the stokes parameters for the samples
# take the data summary of the stokes params

# calculate GLCM fetaures for each samples

# export samples to csv for further analysis
