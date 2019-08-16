from __future__ import division
import os
import cv2
import numpy as np
import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def readdata(dirpath):
    imgs = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360]

    for index, img in enumerate(imgs):
        data = np.array(cv2.imread(dirpath + '/' + str(img) + '.jpg', 0), dtype=np.float32)

        if (index == 0):
            dataset = np.array(data.flatten())
        else:
            data = data.flatten()
            dataset = np.column_stack((dataset, data))

    return dataset

def plotMMelements(dataset, theta, marker):
    for pxs in dataset:
        A = (1 / 18) * np.sum(pxs)
        B = np.array([])
        C = np.array([])
        D = np.array([])

        for index, px in enumerate(pxs):
            B = np.append(B, (px * np.sin(2 * index * theta)))
            C = np.append(C, (px * np.cos(4 * index * theta)))
            D = np.append(D, (px * np.sin(4 * index * theta)))

        B = (1/9) * np.sum(B)
        C = (1/9) * np.sum(C)
        D = (1/9) * np.sum(D)

        D0 = A - C
        D1 = (2 * C)
        D2 = (2 * D)
        D3 = B

        print '========='
        print 'D1: ', D1
        print 'D2: ', D2
        print 'D3: ', D3
        print '========='

        ax.scatter(D1, D2, D3, marker=marker)

def main():
    #TODO remove this array
    imgs = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360]

    rawnewData = readdata('./exp-06-27-17-specular-new-type1')
    rawoldData = readdata('./exp-06-27-17-specular-old-type1')
    theta = 20

    newData = random.sample(rawnewData, 100)
    oldData = random.sample(rawoldData, 100)

    print type(newData)

    # TODO add this back for plotting
    # plotMMelements(newData, theta, 'x')
    # plotMMelements(oldData, theta, 'o')

    # TODO Remove this for not graphing single px scatter plots
    # for pxs in newData:
    #     for index, px in enumerate(pxs):
    #         plt.scatter(px, imgs[index])
    print "NEW DATA", newData[0]
    imgs = np.array(imgs)
    print "IMAGES", imgs

    alldata = newData[0]

    # z = np.polyfit(imgs, data, 3)
    # f = np.poly1d(z)
    #
    # x = np.linspace(imgs[0], imgs[-1], 50)
    # y = f(x)

    # plt.scatter(t, data, marker='x')
    # plt.scatter(x, y)
    # plt.show()

    N = 1000 # number of data points
    t = np.linspace(0, 2*np.pi, N)

    guess_mean = np.mean(data)
    guess_std = 3*np.std(data)/(2**0.5)
    guess_phase = 0

    print "MEAN", guess_mean

    # data_first_guess = guess_std * np.sin(imgs + guess_phase) + guess_mean

    data_first_guess = guess_mean + guess_std*np.cos(4*imgs)

    print "FIRST_GUESS", data_first_guess

    plt.scatter(imgs, data_first_guess, color="r")
    plt.show()

if __name__ == "__main__":
    # TODO Add this back for 3d plotting
    # fig = plt.figure()
    # ax = fig.gca(projection='3d')

    plt.xlabel('D1')
    plt.ylabel('D2')
    main()
