from __future__ import division
import numpy as np

import cv2
import os
from sklearn.feature_extraction import image
import matplotlib.pyplot as plt
from skimage.feature import greycomatrix, greycoprops

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

# img_dirs = ['../../app/data/american-ash-1-white-diffuse', '../../app/data/sugar-maple-1-white-diffuse', '../../app/data/red-oak-1-white-diffuse']
# labels = ['American Ash', 'Sugar Maple', 'Red Oak']
# labels = ['80 Grit', '100 Grit', '150 Grit', '220 Grit']
# labels = ['American Ash 1', 'American Ash 2', 'American Ash 3', 'Sugar Maple 1', 'Sugar Maple 2','Sugar Maple 3', 'Red Oak 1', 'Red Oak 2', 'Red Oak 3']
# img_dirs = ['../../app/data/american-ash-1-white-specular','../../app/data/american-ash-2-white-specular', '../../app/data/american-ash-3-white-specular', '../../app/data/sugar-maple-1-white-specular','../../app/data/sugar-maple-2-white-specular','../../app/data/sugar-maple-3-white-specular', '../../app/data/red-oak-1-white-specular', '../../app/data/red-oak-2-white-specular', '../../app/data/red-oak-3-white-specular']
#


# img_dirs = ['../../app/data/grit-80-sandpaper-diffuse', '../../app/data/grit-100-sandpaper-diffuse', '../../app/data/grit-150-sandpaper-diffuse', '../../app/data/grit-220-sandpaper-diffuse']
# labels = ['90%', '99%']
# img_dirs = ['../../app/data/di-1_1-white-specular', '../../app/data/di-2+1-white-specular']

# official specular##################################

# labels = ['Red Oak 0wk', 'Red Oak 1wk' ]
# img_dirs = ['../../app/data/red-oak-3-white-specular', '../../app/data/red-oak-1-white-specular-1wk' ]

# labels = ['American Ash', 'Sugar Maple',  'Red Oak', ]
# img_dirs = ['../../app/data/american-ash-2-white-specular', '../../app/data/sugar-maple-2-white-specular', '../../app/data/red-oak-3-white-specular' ]


######################
# offical diffuse #####################################

# labels = ['American Ash', 'Sugar Maple',  'Red Oak', ]
# img_dirs = ['../../app/data/american-ash-1-white-diffuse', '../../app/data/sugar-maple-2-white-diffuse', '../../app/data/red-oak-3-white-diffuse' ]
#
# labels = ['Red Oak 0wk', 'Red Oak 1wk' ]
# img_dirs = ['../../app/data/red-oak-1-white-diffuse', '../../app/data/red-oak-1-white-diffuse-1wk' ]



###################################

labels = ['Red Oak 0wk', 'Red Oak 1wk' ]
img_dirs = ['../../app/data/sugar-maple-1-white-specular', '../../app/data/sugar-maple-1-white-specular-1wk' ]


# markers = ['o', 'x', '*', 'o', 'x', '*', 'o', 'x', '*']
markers = ['o', 'x', '*', 'o', 'x', '*', 'o', 'x', '*']

colors = ['r', 'b', 'g', 'c']
# colors = ['r', 'r', 'r', 'b', 'b', 'b', 'g', 'g', 'g']

size = 9
count = 100

for index, img_dir in enumerate(img_dirs):
    H, V, P, M = [cv2.imread(os.path.join(img_dir, filter_angle_img), 1) for filter_angle_img in ['H.png', 'V.png', 'P.png', 'M.png']]
    # do individual channels
    H_b, H_g, H_r = cv2.split(H)
    V_b, V_g, V_r = cv2.split(V)
    P_b, P_g, P_r = cv2.split(P)
    M_b, M_g, M_r = cv2.split(M)

    H_b_samples, H_g_samples, H_r_samples, V_b_samples, V_g_samples, V_r_samples, P_b_samples, P_g_samples, P_r_samples, M_b_samples, M_g_samples, M_r_samples = [image.extract_patches_2d(filter_angle, (size, size), count, 1) for filter_angle in [H_b, H_g, H_r, V_b, V_g, V_r, P_b, P_g, P_r, M_b, M_g, M_r]]

    img_name = labels[index] + '-H.png'
    cv2.imwrite(img_name, H_b_samples[0] * 255)

    H_b_texture, H_g_texture, H_r_texture = [extract_texture(samples) for samples in [H_b_samples.astype(np.uint8), H_g_samples.astype(np.uint8), H_r_samples.astype(np.uint8)]]
    V_b_texture, V_g_texture, V_r_texture = [extract_texture(samples) for samples in [V_b_samples.astype(np.uint8), V_g_samples.astype(np.uint8), V_r_samples.astype(np.uint8)]]
    P_b_texture, P_g_texture, P_r_texture = [extract_texture(samples) for samples in [P_b_samples.astype(np.uint8), P_g_samples.astype(np.uint8), P_r_samples.astype(np.uint8)]]
    M_b_texture, M_g_texture, M_r_texture = [extract_texture(samples) for samples in [M_b_samples.astype(np.uint8), M_g_samples.astype(np.uint8), M_r_samples.astype(np.uint8)]]

    plt.figure(1)
    plt.suptitle('Texture Analysis of BGR Channels', fontsize=20)
    plt.xlabel('Dissimilarity')
    plt.ylabel('Correlation')
    plt.title('H Filter, Blue Channel Texture')
    plt.subplot(131)
    plt.scatter(H_b_texture[:,0], H_b_texture[:,2], marker=markers[index], label=labels[index], color=colors[index])
    plt.xlabel('Dissimilarity')
    plt.ylabel('Correlation')
    plt.title('H Filter, Green Channel Texture')
    plt.subplot(132)
    plt.scatter(H_g_texture[:,0], H_g_texture[:,2], marker=markers[index], label=labels[index], color=colors[index])
    plt.xlabel('Dissimilarity')
    plt.ylabel('Correlation')
    plt.title('H Filter, Red Channel Texture')
    plt.subplot(133)
    plt.scatter(H_r_texture[:,0], H_r_texture[:,2], marker=markers[index], label=labels[index], color=colors[index])
    plt.legend()

    plt.figure(2)
    plt.suptitle('Texture Analysis of BGR Channels', fontsize=20)
    plt.subplot(131)
    plt.xlabel('Dissimilarity')
    plt.ylabel('Correlation')
    plt.title('V Filter, Blue Channel Texture')
    plt.scatter(V_b_texture[:,0], V_b_texture[:,2], marker=markers[index], label=labels[index], color=colors[index])

    plt.subplot(132)
    plt.xlabel('Dissimilarity')
    plt.ylabel('Correlation')
    plt.title('V Filter, Green Channel Texture')
    plt.scatter(V_g_texture[:,0], V_g_texture[:,2], marker=markers[index], label=labels[index], color=colors[index])

    plt.subplot(133)
    plt.xlabel('Dissimilarity')
    plt.ylabel('Correlation')
    plt.title('V Filter, Red Channel Texture')
    plt.scatter(V_r_texture[:,0], V_r_texture[:,2], marker=markers[index], label=labels[index], color=colors[index])
    plt.legend()

    plt.figure(3)
    plt.suptitle('Texture Analysis of BGR Channels', fontsize=20)
    plt.subplot(131)
    plt.xlabel('Dissimilarity')
    plt.ylabel('Correlation')
    plt.title('P Filter, Blue Channel Texture')
    plt.scatter(P_b_texture[:,0], P_b_texture[:,2], marker=markers[index], label=labels[index], color=colors[index])

    plt.subplot(132)
    plt.xlabel('Dissimilarity')
    plt.ylabel('Correlation')
    plt.title('P Filter, Green Channel Texture')
    plt.scatter(P_g_texture[:,0], P_g_texture[:,2], marker=markers[index], label=labels[index], color=colors[index])

    plt.subplot(133)
    plt.xlabel('Dissimilarity')
    plt.ylabel('Correlation')
    plt.title('P Filter, Red Channel Texture')
    plt.scatter(P_r_texture[:,0], P_r_texture[:,2], marker=markers[index], label=labels[index], color=colors[index])
    plt.legend()

    plt.figure(4)
    plt.suptitle('Texture Analysis of BGR Channels', fontsize=20)
    plt.subplot(131)
    plt.xlabel('Dissimilarity')
    plt.ylabel('Correlation')
    plt.title('M Filter, Blue Channel Texture')
    plt.scatter(M_b_texture[:,0], M_b_texture[:,2], marker=markers[index], label=labels[index], color=colors[index])

    plt.subplot(132)
    plt.xlabel('Dissimilarity')
    plt.ylabel('Correlation')
    plt.title('M Filter, Green Channel Texture')
    plt.scatter(M_g_texture[:,0], M_g_texture[:,2], marker=markers[index], label=labels[index], color=colors[index])

    plt.subplot(133)
    plt.xlabel('Dissimilarity')
    plt.ylabel('Correlation')
    plt.title('M Filter, Red Channel Texture')
    plt.scatter(M_r_texture[:,0], M_r_texture[:,2], marker=markers[index], label=labels[index], color=colors[index])
    plt.legend()

plt.show()
