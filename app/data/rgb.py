from __future__ import division

import numpy as np
import cv2

'brown-oak.png'

def rgri(image):
    img = cv2.imread(image)

    b, g, r = cv2.split(img)

    rgri = np.mean(r) / np.mean(g)

    print "RGRI: ", rgri

    return rgri


for values, color, channel in zip((r,g,b), ('r','g','b'), (2,1,0)):
    testimg = np.zeros((values.shape[0], values.shape[1],3), dtype=np.int)
    testimg[:,:,channel] = values
    # cv2.imshow('test', testimg)

#     # save image to current directory in rgb folder
