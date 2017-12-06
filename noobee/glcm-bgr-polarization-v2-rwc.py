"""
This version will perform the glcm texture analysis on the original H, V, P, M filters for rwc csv generation
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
img_dir = '../app/data/di-2_2-white-specular'
rwc = 98.2308
size = 75
count = 50
# rwc= np.tile(np.array([97.6220]),(count,1))


H, V, P, M = [cv2.imread(os.path.join(img_dir, filter_angle_img), 1) for filter_angle_img in ['H.png', 'V.png', 'P.png', 'M.png']]


H_b, H_g, H_r = cv2.split(H)
V_b, V_g, V_r = cv2.split(V)
P_b, P_g, P_r = cv2.split(P)
M_b, M_g, M_r = cv2.split(M)
# cv2.imshow('sdf',S1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



S1_b = calculate_stokes((H_b, V_b))
S1_g = calculate_stokes((H_g, V_g))
S1_r = calculate_stokes((H_r, V_r))

S2_b = calculate_stokes((P_b, M_b))
S2_g = calculate_stokes((P_g, M_g))
S2_r = calculate_stokes((P_r, M_r))

S1_b_summary = datasummary(S1_b)
S1_g_summary = datasummary(S1_g)
S1_r_summary = datasummary(S1_r)

S2_b_summary = datasummary(S2_b)
S2_g_summary = datasummary(S2_g)
S2_r_summary = datasummary(S2_r)
print S1_r_summary
H_b_samples, H_g_samples, H_r_samples, V_b_samples, V_g_samples, V_r_samples, P_b_samples, P_g_samples, P_r_samples, M_b_samples, M_g_samples, M_r_samples = [image.extract_patches_2d(filter_angle, (size, size), count, 1) for filter_angle in [H_b, H_g, H_r, V_b, V_g, V_r, P_b, P_g, P_r, M_b, M_g, M_r]]
#
H_b_texture, H_g_texture, H_r_texture = [extract_texture(sample) for sample in [H_b_samples.astype(np.uint8), H_g_samples.astype(np.uint8), H_r_samples.astype(np.uint8)]]
V_b_texture, V_g_texture, V_r_texture = [extract_texture(sample) for sample in [V_b_samples.astype(np.uint8), V_g_samples.astype(np.uint8), V_r_samples.astype(np.uint8)]]
P_b_texture, P_g_texture, P_r_texture = [extract_texture(sample) for sample in [P_b_samples.astype(np.uint8), P_g_samples.astype(np.uint8), P_r_samples.astype(np.uint8)]]
M_b_texture, M_g_texture, M_r_texture = [extract_texture(sample) for sample in [M_b_samples.astype(np.uint8), M_g_samples.astype(np.uint8), M_r_samples.astype(np.uint8)]]

# H_b_texture = (H_b_texture[:,0] - H_b_texture[:,0].min())/(H_b_texture[:,0].max() - H_b_texture[:,0].min())
# H_g_texture = (H_g_texture - H_g_texture.min())/(H_g_texture.max() - H_g_texture.min())
# H_r_texture = (H_r_texture - H_r_texture.min())/(H_r_texture.max() - H_r_texture.min())
#
# V_b_texture = (V_b_texture - V_b_texture.min())/(V_b_texture.max() - V_b_texture.min())
# V_g_texture = (V_g_texture - V_g_texture.min())/(V_g_texture.max() - V_g_texture.min())
# V_r_texture = (V_r_texture - V_r_texture.min())/(V_r_texture.max() - V_r_texture.min())
#
# P_b_texture = (P_b_texture - P_b_texture.min())/(P_b_texture.max() - P_b_texture.min())
# P_g_texture = (P_g_texture - P_g_texture.min())/(P_g_texture.max() - P_g_texture.min())
# P_r_texture = (P_r_texture - P_r_texture.min())/(P_r_texture.max() - P_r_texture.min())
#
# M_b_texture = (M_b_texture - M_b_texture.min())/(M_b_texture.max() - M_b_texture.min())
# M_g_texture = (M_g_texture - M_g_texture.min())/(M_g_texture.max() - M_g_texture.min())
# M_r_texture = (M_r_texture - M_r_texture.min())/(M_r_texture.max() - M_r_texture.min())


# H_b_diss = np.mean(H_b_texture[:,0] - H_b_texture[:,0].min())/(H_b_texture[:,0].max() - H_b_texture[:,0].min())
# H_b_contrast = np.mean(H_b_texture[:,1] - H_b_texture[:,1].min())/(H_b_texture[:,1].max() - H_b_texture[:,1].min())
# H_b_corr = np.mean(H_b_texture[:,2] - H_b_texture[:,2].min())/(H_b_texture[:,2].max() - H_b_texture[:,2].min())
# H_b_energy = np.mean(H_b_texture[:,3] - H_b_texture[:,3].min())/(H_b_texture[:,3].max() - H_b_texture[:,3].min())
# H_g_diss = np.mean(H_g_texture[:,0] - H_g_texture[:,0].min())/(H_g_texture[:,0].max() - H_g_texture[:,0].min())
# H_g_contrast = np.mean(H_g_texture[:,1] - H_g_texture[:,1].min())/(H_g_texture[:,1].max() - H_g_texture[:,1].min())
# H_g_corr = np.mean(H_g_texture[:,2] - H_g_texture[:,2].min())/(H_g_texture[:,2].max() - H_g_texture[:,2].min())
# H_g_energy = np.mean(H_g_texture[:,3] - H_g_texture[:,3].min())/(H_g_texture[:,3].max() - H_g_texture[:,3].min())
# H_r_diss = np.mean(H_r_texture[:,0] - H_r_texture[:,0].min())/(H_r_texture[:,0].max() - H_r_texture[:,0].min())
# H_r_contrast = np.mean(H_r_texture[:,1] - H_r_texture[:,1].min())/(H_r_texture[:,1].max() - H_r_texture[:,1].min())
# H_r_corr = np.mean(H_r_texture[:,2] - H_r_texture[:,2].min())/(H_r_texture[:,2].max() - H_r_texture[:,2].min())
# H_r_energy = np.mean(H_r_texture[:,3] - H_r_texture[:,3].min())/(H_r_texture[:,3].max() - H_r_texture[:,3].min())
H_b_diss = np.mean(H_b_texture[:,0])
H_b_contrast = np.mean(H_b_texture[:,1])
H_b_corr = np.mean(H_b_texture[:,2])
H_b_energy = np.mean(H_b_texture[:,3])
H_g_diss = np.mean(H_g_texture[:,0])
H_g_contrast = np.mean(H_g_texture[:,1])
H_g_corr = np.mean(H_g_texture[:,2])
H_g_energy = np.mean(H_g_texture[:,3])
H_r_diss = np.mean(H_r_texture[:,0])
H_r_contrast = np.mean(H_r_texture[:,1])
H_r_corr = np.mean(H_r_texture[:,2])
H_r_energy = np.mean(H_r_texture[:,3])

V_b_diss = np.mean(V_b_texture[:,0])
V_b_contrast = np.mean(V_b_texture[:,1])
V_b_corr = np.mean(V_b_texture[:,2])
V_b_energy = np.mean(V_b_texture[:,3])
V_g_diss = np.mean(V_g_texture[:,0])
V_g_contrast = np.mean(V_g_texture[:,1])
V_g_corr = np.mean(V_g_texture[:,2])
V_g_energy = np.mean(V_g_texture[:,3])
V_r_diss = np.mean(V_r_texture[:,0])
V_r_contrast = np.mean(V_r_texture[:,1])
V_r_corr = np.mean(V_r_texture[:,2])
V_r_energy = np.mean(V_r_texture[:,3])

P_b_diss = np.mean(P_b_texture[:,0])
P_b_contrast = np.mean(P_b_texture[:,1])
P_b_corr = np.mean(P_b_texture[:,2])
P_b_energy = np.mean(P_b_texture[:,3])
P_g_diss = np.mean(P_g_texture[:,0])
P_g_contrast = np.mean(P_g_texture[:,1])
P_g_corr = np.mean(P_g_texture[:,2])
P_g_energy = np.mean(P_g_texture[:,3])
P_r_diss = np.mean(P_r_texture[:,0])
P_r_contrast = np.mean(P_r_texture[:,1])
P_r_corr = np.mean(P_r_texture[:,2])
P_r_energy = np.mean(P_r_texture[:,3])

M_b_diss = np.mean(M_b_texture[:,0])
M_b_contrast = np.mean(M_b_texture[:,1])
M_b_corr = np.mean(M_b_texture[:,2])
M_b_energy = np.mean(M_b_texture[:,3])
M_g_diss = np.mean(M_g_texture[:,0])
M_g_contrast = np.mean(M_g_texture[:,1])
M_g_corr = np.mean(M_g_texture[:,2])
M_g_energy = np.mean(M_g_texture[:,3])
M_r_diss = np.mean(M_r_texture[:,0])
M_r_contrast = np.mean(M_r_texture[:,1])
M_r_corr = np.mean(M_r_texture[:,2])
M_r_energy = np.mean(M_r_texture[:,3])


print S1_b_summary
print rwc

# features = np.concatenate((rwc, S1_b_summary, S1_g_summary, S1_r_summary, S2_b_summary, S2_g_summary, S2_r_summary), axis=1)
features = [[rwc, S1_b_summary[0], S1_g_summary[0], S1_r_summary[0], S2_b_summary[0], S2_g_summary[0], S2_r_summary[0], S1_b_summary[1], S1_g_summary[1], S1_r_summary[1], S2_b_summary[1], S2_g_summary[1], S2_r_summary[1], H_b_diss, V_b_diss, P_b_diss, M_b_diss, H_b_contrast, V_b_contrast, P_b_contrast, M_b_contrast, H_b_corr, V_b_corr, P_b_corr, M_b_corr, H_b_energy, V_b_energy, P_b_energy, M_b_energy ]]

print features
with open('rwc-specular-plant2.csv', 'a') as f:
    np.savetxt(f, features, delimiter=',', fmt="%g")
f.close()
# print np.std(S1_r)
# plt.hist(createhistogram(S1_r, bins=np.linspace(-1,1,200)))
# plt.show()

# calculate the stokes parameters for the samples
# take the data summary of the stokes params

# calculate GLCM fetaures for each samples

# export samples to csv for further analysis
