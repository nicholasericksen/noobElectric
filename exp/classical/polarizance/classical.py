from __future__ import division
from mpl_toolkits.mplot3d import Axes3D
import random
import cv2
import numpy as np
import matplotlib.pyplot as plt

# imgs = [14, 34, 54, 74, 94, 114, 134, 154, 174, 194, 214, 234, 254, 274,294, 314, 334, 354]
imgs = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360]
pxs = np.array([])

for index, img in enumerate(imgs):
    image = cv2.imread('../diattenuation/exp-06-27-17-new-diffuse/' + str(img) + '.jpg', 0)
    data = np.array(image, dtype=np.float32)

    if (index == 0):
        dataset = np.array(data.flatten())
    else:
        data = data.flatten()
        dataset = np.column_stack((dataset, data))


for index, img in enumerate(imgs):
    image2 = cv2.imread('../diattenuation/exp-06-27-17-new-diffuse/' + str(img) + '.jpg', 0)
    data2 = np.array(image2, dtype=np.float32)

    if (index == 0):
        dataset2 = np.array(data2.flatten())
    else:
        data2 = data2.flatten()
        dataset2 = np.column_stack((dataset2, data2))

fig = plt.figure()
ax = fig.gca(projection='3d')

plt.xlabel('S1')
plt.ylabel('S2')

def getStokes(pxs, imgs, color, marker, label):
    dft = np.fft.fft(pxs)
    print "DFT: ", dft
    print '=============================='
    dc = np.mean(pxs)
    print "Mean: ", dc
    print "=============================="
    n = pxs.size
    freq = np.fft.fftfreq(n)

    print "frequency: ", freq
    print '=============================='
    raw = np.sum(pxs)

    A = (2 / n) * raw

    print "A: ", A

    Braw = np.array([])
    Craw = np.array([])
    Draw = np.array([])

    for index, px in enumerate(pxs):
        Bcalc = px * np.sin(2*imgs[index])
        Braw = np.append(Braw, Bcalc)

        Ccalc = px * np.cos(4*imgs[index])
        Craw = np.append(Craw, Ccalc)

        Dcalc = px * np.sin(4*imgs[index])
        Draw = np.append(Draw, Dcalc)

    B = (4 / n) * (np.sum(Braw))
    C = (4 / n) * (np.sum(Craw))
    D = (4 / n) * (np.sum(Draw))

    print "B: ", B
    print "C: ", C
    print "D: ", D

    S0 = A - C
    S1 = 2 * C
    S2 = 2 * D
    S3 = B

    # note this is not normalized
    S0norm = S0
    S1norm = S1
    S2norm = S2
    S3norm = S3

    print '+++++++++'
    print 'S0: ', S0norm
    print 'S1: ', S1norm
    print 'S2: ', S2norm
    print 'S3: ', S3norm

    ax.scatter(S1norm, S2norm, S3norm, color=color, marker=marker, s=100)

random_dataset = random.sample(dataset, 1000)
for pxs in random_dataset:
    getStokes(pxs, imgs, "y", "o", "new")

random_dataset2 = random.sample(dataset2, 1000)
for pxs in random_dataset2:
    getStokes(pxs, imgs, "g", "x", "old")

plt.legend(loc=0)
plt.show()
