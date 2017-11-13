"""
Binary classification of two images using texture based feature extraction

This module is intended to take two input images that represent different
surfaces, extract samples from each color channel, extract texture features,
and classify the surface texture using Support Vector Classification.

Examples:
    In this example the red color channel is shown to classify texture
    better than the other color channels.

    As a script:
        $ python texture.py img1.png img2.png
            > ====================
            > Channel:  blue
            > Score:  0.85
            > ====================
            > ====================
            > Channel:  green
            > Score:  0.85
            > ====================
            > ====================
            > Channel:  red
            > Score:  0.9
            > ====================

    As an import:
        >>> import texture
        >>> results = texture.classify('img1.png', 'im2.png')
        >>> print results
        >>> (0.85, 0.85, 0.9)
"""
from  __future__ import division

import cv2
import numpy as np

from sklearn import svm
from sklearn.feature_extraction import image
from skimage.feature import greycomatrix, greycoprops

def extract_bgr_samples(filename, size, count):
    """
    Extract random samples from b, g, r image channels.

    Args:
        filename (str): Location to the image filename.
        size (int): The length/width of the square sample.
        count (int): The number of samples to generate.
    Returns:
        tuple: Random samples from each color channel.
    """
    img = cv2.imread(filename, 1)
    blue_channel, green_channel, red_channel = cv2.split(img)

    b_samples = image.extract_patches_2d(blue_channel, (size, size), count, 1)
    g_samples = image.extract_patches_2d(green_channel, (size, size), count, 1)
    r_samples = image.extract_patches_2d(red_channel, (size, size), count, 1)

    return b_samples, g_samples, r_samples

def extract_texture(samples):
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

def svc_texture(channel, texture_1, texture_2):
    """
    A Support Vector Classification using texture features.

    Args:
        label (str): Description.
        texture_1 (array): Texture features in the first class.
        texture_2 (array): Texture features in the second class.
    Returns:
        double: The successful classification probability out of 1.0.
    """
    if texture_1.shape[0] is not texture_2.shape[0]:
        return "Datasets not the same size."

    data_size = texture_1.shape[0]
    training_size = int(data_size * 0.9)
    testing_size = data_size - training_size

    # Create training data
    X = np.vstack((texture_1[:training_size], texture_2[:training_size]))
    y = np.append(np.zeros(training_size), np.ones(training_size))

    # Create testing data
    testing_features = np.vstack((texture_1[training_size:], texture_2[training_size:]))
    testing_labels = np.append(np.zeros(testing_size), np.ones(testing_size))

    # Fit data to classifier
    clf = svm.SVC()
    fit = clf.fit(X, y)
    score = fit.score(testing_features, testing_labels)

    print "===================="
    print "Channel: ", channel
    print "Score: ", score
    print "===================="

    return score

def classify(img_src_1, img_src_2):
    """
    Texture classification comparision for Red, Green, and Blue color image channels

    Args:
        img_src_1 (str): The path to the first texture image
        img_src_2 (str): The path to the second texture image
    Returns:
        tuple: Blue channel accuracy, Green channel accuracy, Red channel accuracy
    """
    channels_1 = extract_bgr_samples(img_src_1, 95, 100)
    channels_2 = extract_bgr_samples(img_src_2, 95, 100)

    texture_1 = [extract_texture(channel) for channel in channels_1]
    texture_2 = [extract_texture(channel) for channel in channels_2]

    # Calculate the classification scores for each channel
    blue_score = svc_texture('blue', texture_1[0], texture_2[0])
    green_score = svc_texture('green', texture_1[1], texture_2[1])
    red_score = svc_texture('red', texture_1[2], texture_2[2])

    return blue_score, green_score, red_score

if __name__ == '__main__':
    import sys
    classify(str(sys.argv[1]), str(sys.argv[2]))
