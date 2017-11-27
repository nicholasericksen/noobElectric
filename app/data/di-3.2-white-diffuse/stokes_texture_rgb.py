from __future__ import division

import cv2
import numpy as np
import matplotlib.pyplot as plt

def calculate_stokes(H, V):
    H = H.astype(np.int16)
    V = V.astype(np.int16)

    S1 = (H - V) / (H + V)

    # These represent values that have not been illuminated by the source
    # ie they are the product of masking and shadowing.
    S1[~np.isfinite(S1)] = 0

    return S1

H = cv2.imread('../di-3_1-white-specular/H.png', 1)
V = cv2.imread('../di-3_1-white-specular/V.png', 1)
print H.shape
Hb, Hg, Hr = cv2.split(H)
Vb, Vg, Vr = cv2.split(V)

S1 = calculate_stokes(H, V)

S1b = calculate_stokes(Hb, Vb)
S1g = calculate_stokes(Hg, Vg)
S1r = calculate_stokes(Hr, Vr)

cv2.imshow('S1r', np.abs(S1r))
cv2.imshow('S1g', np.abs(S1g))
cv2.imshow('S1b', np.abs(S1b))
# print S1g
print '#####################'
img = np.array(np.abs(np.dstack((S1b, S1g, S1r))))
print img

cv2.imshow('S1', np.abs(S1))
# cv2.imwrite('img.png', img * 255)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)


cv2.imshow("S1b", S1b)
cv2.imshow("S1g", S1g)
cv2.imshow("S1r", S1r)

cv2.waitKey(0)
cv2.destroyAllWindows()
print S1b
plt.hist(S1.ravel(), bins=np.linspace(-1,1,200))
plt.show()
plt.hist(S1b.ravel(), bins=np.linspace(-1,1,200))
plt.show()
plt.hist(S1g.ravel(), bins=np.linspace(-1,1,200))
plt.show()
plt.hist(S1r.ravel(), bins=np.linspace(-1,1,200))
plt.show()
