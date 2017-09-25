from __future__ import division
import cv2
import numpy as np
import matplotlib.pyplot as plt

np.seterr(divide='ignore', invalid='ignore')

H = np.array(cv2.imread('./0.jpg', 0), dtype=np.float32)
V = np.array(cv2.imread('./90.jpg', 0), dtype=np.float32)
P = np.array(cv2.imread('./45.jpg', 0), dtype=np.float32)
M = np.array(cv2.imread('./135.jpg', 0), dtype=np.float32)

S0 = np.array(cv2.imread('./clear.jpg', 0), dtype=np.float32)

S1 = (H - V) / (H+V)
S2 = (P - M) / (P+M)

S1[np.isnan(S1)] = 0
S2[np.isnan(S2)] = 0

plt.scatter(S1, S2, color='b', marker='o', label='Basil')

Hp = np.array(cv2.imread('../exp-07-pepper/0.jpg', 0), dtype=np.float32)
Vp = np.array(cv2.imread('../exp-07-pepper/90.jpg', 0), dtype=np.float32)
Pp = np.array(cv2.imread('../exp-07-pepper/45.jpg', 0), dtype=np.float32)
Mp = np.array(cv2.imread('../exp-07-pepper/135.jpg', 0), dtype=np.float32)

S0p = np.array(cv2.imread('./clear.jpg', 0), dtype=np.float32)

S1p = (Hp - Vp) / (Hp + Vp)
S2p = (Pp - Mp) / (Pp + Mp)

S1p[np.isnan(S1p)] = 0
S2p[np.isnan(S2p)] = 0

print "======Basil======"
print "S1: ", S1
print "S2: ", S2
print "=================="
plt.scatter(S1p, S2p, color='g', marker='x', label='Pepper')

plt.legend(loc='upper right')
plt.show()


plt.hist(S1.ravel())
plt.hist(S1p.ravel())

plt.show()

plt.hist(S2)
plt.hist(S2p)

plt.show()
