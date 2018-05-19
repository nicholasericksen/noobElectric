from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.feature_extraction import image

def bgr_split(img):
    b = img[:,:,0]
    g = img[:,:,1]
    r = img[:,:,2]

    return b, g, r

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
    img = cv2.imread('../../../../app/data/di-3^5-white-specular/' + filename, 1)
    samples = image.extract_patches_2d(img, (size, size), count, 1)
    cv2.imwrite('sample.png', samples[0])
    b, g, r = bgr_split(samples[0])

    return b, g, r

def normed(data):
    print "data", data
    size = 75*75;
    minimum = np.min(data)
    maximum = np.max(data)
    print "Maximum", maximum
    print "Minimum", minimum
    #
    # norm = (data - minimum) / (maximum - minimum)
    #
    norm = [float(i) / size for i in data]
    # print "Normded", normed
    # norm = [float(i)/sum(data) for i in data]
    return norm

def plot_bgr(bgr, title):
    bins = np.arange(0,255, 1)

    plt.subplot(121)
    plt.title('Sample')
    # img = np.array(np.abs(np.dstack((bgr[0], bgr[1], bgr[2]))))
    plt.imshow(bgr[0], 'gray')
    plt.ylabel('pxs', fontsize=14)
    plt.xlabel('pxs', fontsize=14)
    plt.subplot(122)
    plt.title('Grey Level Histogram - Blue Channel', fontsize=16)
    plt.hist(bgr[0].ravel(), bins, color='blue')
    plt.ylabel('Number of pxs', fontsize=14)
    plt.xlabel('Digital Number', fontsize=14)
    plt.suptitle(title + ' Polarization Blue Channel Sample & Histogram', fontsize=18)
    plt.show()

    plt.title('g')
    plt.subplot(121)
    plt.imshow(bgr[1], 'gray')
    plt.ylabel('pxs')
    plt.xlabel('pxs')
    plt.subplot(122)
    plt.hist(bgr[1].ravel(), bins, color='green')
    plt.ylabel('Number of pxs')
    plt.xlabel('Digital Number')
    plt.suptitle(title + ' Polarization Green Channel Sample & Histogram', fontsize=16)
    plt.show()

    plt.title('r')
    plt.subplot(121)
    plt.imshow(bgr[2], 'gray')
    plt.ylabel('pxs')
    plt.xlabel('pxs')
    plt.subplot(122)
    plt.hist(bgr[2].ravel(), bins, color='red')
    plt.ylabel('Number of pxs')
    plt.xlabel('Digital Number')
    plt.suptitle(title + ' Polarization Red Channel Sample & Histogram', fontsize=16)
    plt.show()

def calculate_stokes((P1, P2)):
    P1 = P1.astype(np.float32)
    P2 = P2.astype(np.float32)
    print "P1", P1
    print "P2", P2
    P1[np.abs(P1) < 1] = 0
    P2[np.abs(P2) < 1] = 0

    S = (P1 - P2) / (P1 + P2)

    # These represent values that have not been illuminated by the source
    # ie they are the product of masking and shadowing.
    S[~np.isfinite(S)] = 0

    return S

H, V, P, M = [extract_bgr_samples(img, 75, 1) for img in ['H.png', 'V.png', 'P.png', 'M.png']]
#
# plot_bgr(H, 'H')
# plot_bgr(V, 'V')
# plot_bgr(P, 'P')
# plot_bgr(M, 'M')
S1b = calculate_stokes((H[0], V[0]))
S1g = calculate_stokes((H[1], V[1]))
S1r = calculate_stokes((H[2], V[2]))

def createhistogram(raw_data, bins='auto'):
    data = raw_data.ravel()
    print "DATA", data
    # bins = np.arange(np.floor(data.min()),np.ceil(data.max()))
    hist = np.histogram(data, normed=1)
    # bins = bins.tolist()
    # / len(data) to normalize to 1
    # values = hist / len(data)
    values = [x / len(data) for x in hist[0]]
    print "VALUES", hist[0]
    print len(data)

    # Convert the tuples into arrays for smaller formatting
    # zipped = [list(t) for t in zip(bins, values.tolist())]
    zipped = values
    return hist


SIZE = 75 * 75
weights_b = (np.ones_like(S1b)/float(len(S1b))).ravel()
weights_g = (np.ones_like(S1g)/float(len(S1g))).ravel()
weights_r = (np.ones_like(S1r)/float(len(S1r))).ravel()
print weights_b.shape


s1b = createhistogram(S1b)
print "BLUEL", S1b.ravel()
plt.suptitle('BGR Polarization', fontsize=18)
plt.subplot(231)
plt.title('S1 Blue Channel')
plt.xlabel('Stokes Polarization')
plt.ylabel('Probability')
plt.hist(S1b.ravel(), normed=True, color='blue')
plt.subplot(234)
plt.xlabel('Polarization Image')
plt.imshow(np.abs(S1b), 'gray')
plt.axis('off')

plt.subplot(232)
plt.title('S1 Green Channel')
plt.xlabel('Stokes Polarization')
plt.ylabel('Probability')
plt.hist(S1g.ravel(), normed=True, color='green')
plt.subplot(235)
plt.imshow(np.abs(S1g), 'gray')
plt.axis('off')

plt.subplot(233)
plt.title('S1 Red Channel')
plt.xlabel('Stokes Polarization')
plt.ylabel('Probability')
plt.hist(S1r.ravel(), normed=True, color='red')
plt.subplot(236)
plt.imshow(np.abs(S1r), 'gray')
plt.axis('off')
plt.show()
