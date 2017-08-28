from __future__ import division
import os
import cv2
import numpy as np

def createdataset(imgs):
    print imgs
    for index, img in enumerate(imgs):
        image = cv2.imread(img, 0)
        data = np.array(image, dtype=np.float32)

        if (index == 0):
            dataset = np.array(data.flatten())
        else:
            data = data.flatten()
            dataset = np.column_stack((dataset, data))
    return dataset

def getStokes(pxs, n):
    imgs = [14, 34, 54, 74, 94, 114, 134, 154, 174, 194, 214, 234, 254, 274,294, 314, 334, 354, 374]
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

    S0norm = S0 / S0
    S1norm = S1 / S0
    S2norm = S2 / S0
    S3norm = S3 / S0

    print '+++++++++'
    print 'S0: ', S0norm
    print 'S1: ', S1norm
    print 'S2: ', S2norm
    print 'S3: ', S3norm

def main(imgpath):
    imgs = []

    for file in os.listdir(imgpath):
        if file.endswith(".jpg"):
            imgs.append(imgpath + '/' + str(file))

    N = len(imgs)
    print N
    step = 360 / N

    data = createdataset(imgs)

    print data[0]
    s = getStokes(data[0], N)

    return s


if __name__ == "__main__":
    main()
