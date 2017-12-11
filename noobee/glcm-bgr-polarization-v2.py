"""
This version will perform the glcm texture analysis on the original H, V, P, M filters
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

    # return np.array([mean, std])
    hist = np.histogram(data, bins=[-1,-.9,-.8,-.7,-.6,-.5,-.4,-.3,-.2,-.1,0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1], density=1)[0]
    print "Hist", hist
    # return np.array([mean, std])
    return hist

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
# labels = ['80 Grit', '100 Grit', '150 Grit', '220 Grit']
# img_dirs = ['../app/data/grit-80-sandpaper-specular', '../app/data/grit-100-sandpaper-specular', '../app/data/grit-150-sandpaper-specular', '../app/data/grit-220-sandpaper-specular']

img_dirs = ['../app/data/american-ash-1-white-diffuse', '../app/data/american-ash-2-white-diffuse','../app/data/american-ash-3-white-diffuse', '../app/data/sugar-maple-1-white-diffuse','../app/data/sugar-maple-2-white-diffuse','../app/data/sugar-maple-3-white-diffuse', '../app/data/red-oak-1-white-diffuse','../app/data/red-oak-2-white-diffuse','../app/data/red-oak-3-white-diffuse']
labels = ['American Ash 1', 'American Ash 2', 'American Ash 3', 'Sugar Maple 1', 'Sugar Maple 2', 'Sugar Maple 3', 'Red Oak 1','Red Oak 2','Red Oak 3']
#
size = 75
count = 100
# H = cv2.imread(os.path.join(img_dir, 'H.png'), 1)
# V = cv2.imread(os.path.join(img_dir, 'V.png'), 1)
# P = cv2.imread(os.path.join(img_dir, 'P.png'), 1)
# M = cv2.imread(os.path.join(img_dir, 'M.png'), 1)
for img_dir in img_dirs:
    print img_dir
    H, V, P, M = [cv2.imread(os.path.join(img_dir, filter_angle_img), 1) for filter_angle_img in ['H.png', 'V.png', 'P.png', 'M.png']]
    # print "H", H
    # S1, S2 = [calculate_stokes(filter_pair) for filter_pair in [(H,V), (P,M)]]
    # # print "S1", cv2.split(S1)
    # S1_b, S1_g, S1_r = [cv2.split(S1_sample) for S1_sample in S1]
    # S2_b, S2_g, S2_r = [cv2.split(S2_sample) for S2_sample in S2]
    print H
    H_b, H_g, H_r = cv2.split(H)
    V_b, V_g, V_r = cv2.split(V)
    P_b, P_g, P_r = cv2.split(P)
    M_b, M_g, M_r = cv2.split(M)
    # cv2.imshow('sdf',S1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    # extract samples from image
    H_b_samples, H_g_samples, H_r_samples, V_b_samples, V_g_samples, V_r_samples, P_b_samples, P_g_samples, P_r_samples, M_b_samples, M_g_samples, M_r_samples = [image.extract_patches_2d(filter_angle, (size, size), count, 1) for filter_angle in [H_b, H_g, H_r, V_b, V_g, V_r, P_b, P_g, P_r, M_b, M_g, M_r]]
    # S2_b_samples, S2_g_samples, S2_r_samples = [image.extract_patches_2d(polarization, (size, size), count, 1) for polarization in [S2_b, S2_g, S2_r]]

    # H_b_samples, H_g_samples, H_r_samples = cv2.split(H_samples)
    # V_b_samples, V_g_samples, V_r_samples = cv2.split(V_samples)


    S1_b_samples = calculate_stokes((H_b_samples, V_b_samples))
    S1_g_samples = calculate_stokes((H_g_samples, V_g_samples))
    S1_r_samples = calculate_stokes((H_r_samples, V_r_samples))

    S2_b_samples = calculate_stokes((P_b_samples, M_b_samples))
    S2_g_samples = calculate_stokes((P_g_samples, M_g_samples))
    S2_r_samples = calculate_stokes((P_r_samples, M_r_samples))

    S1_b_summary = [datasummary(sample) for sample in S1_b_samples]
    S1_g_summary = [datasummary(sample) for sample in S1_g_samples]
    S1_r_summary = [datasummary(sample) for sample in S1_r_samples]

    S2_b_summary = [datasummary(sample) for sample in S2_b_samples]
    S2_g_summary = [datasummary(sample) for sample in S2_g_samples]
    S2_r_summary = [datasummary(sample) for sample in S2_r_samples]
    print S1_r_summary


    H_b_texture, H_g_texture, H_r_texture = [extract_texture(samples) for samples in [H_b_samples.astype(np.uint8), H_g_samples.astype(np.uint8), H_r_samples.astype(np.uint8)]]
    V_b_texture, V_g_texture, V_r_texture = [extract_texture(samples) for samples in [V_b_samples.astype(np.uint8), V_g_samples.astype(np.uint8), V_r_samples.astype(np.uint8)]]
    P_b_texture, P_g_texture, P_r_texture = [extract_texture(samples) for samples in [P_b_samples.astype(np.uint8), P_g_samples.astype(np.uint8), P_r_samples.astype(np.uint8)]]
    M_b_texture, M_g_texture, M_r_texture = [extract_texture(samples) for samples in [M_b_samples.astype(np.uint8), M_g_samples.astype(np.uint8), M_r_samples.astype(np.uint8)]]
    # S2_b_texture, S2_g_texture, S2_r_texture = [extract_texture(samples) for samples in [S2_b_samples.astype(np.uint8), S2_g_samples.astype(np.uint8), S2_r_samples.astype(np.uint8)]]
    # S1_b_texture = extract_texture(S1_r_samples.astype(np.uint8))
    # print np.concatenate((S1_r_summary, S1_r_texture), axis=1)
    # S1_b_features = np.concatenate((S1_b_summary, S1_b_texture), axis=1)
    # S1_g_features = np.concatenate((S1_g_summary, S1_g_texture), axis=1)
    # S1_r_features = np.concatenate((S1_r_summary, S1_r_texture), axis=1)
    #
    # S2_b_features = np.concatenate((S2_b_summary, S2_b_texture), axis=1)
    # S2_g_features = np.concatenate((S2_g_summary, S2_g_texture), axis=1)
    # S2_r_features = np.concatenate((S2_r_summary, S2_r_texture), axis=1)

    # features = np.concatenate((S1_b_features, S1_g_features, S1_r_features, S2_b_features, S2_g_features, S2_r_features), axis=1)
    features = np.concatenate((S1_b_summary, S1_g_summary, S1_r_summary, S2_b_summary, S2_g_summary, S2_r_summary, H_b_texture, H_g_texture, H_r_texture, V_b_texture, V_g_texture, V_r_texture, P_b_texture, P_g_texture, P_r_texture, M_b_texture, M_g_texture, M_r_texture), axis=1)

    with open('diffuse-trees.csv', 'a') as f:
        np.savetxt(f, features, delimiter=',', fmt="%g")


# print np.std(S1_r)
# plt.hist(createhistogram(S1_r, bins=np.linspace(-1,1,200)))
# plt.show()

# calculate the stokes parameters for the samples
# take the data summary of the stokes params

# calculate GLCM fetaures for each samples

# export samples to csv for further analysis
