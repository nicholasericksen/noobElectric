from __future__ import division

import cv2
import numpy as np
import matplotlib.pyplot as plt

def calculate_stokes(P1, P2):
    P1 = P1.astype(np.int16)
    P2 = P2.astype(np.int16)

    S = (P1 - P2) / (P1 + P2)

    # These represent values that have not been illuminated by the source
    # ie they are the product of masking and shadowing.
    S[~np.isfinite(S)] = 0

    return S

def normed(data):
    print "data", data
    minimum = np.min(data)
    maximum = np.max(data)
    print "Maximum", maximum
    print "Minimum", minimum

    normed = (255*(data - minimum) / (maximum - minimum)) + 255

    print "Normded", normed

    return normed
# H = cv2.imread('../app/data/sugar-maple-2-white-specular/P.png', 1)
# V = cv2.imread('../app/data/sugar-maple-2-white-specular/M.png', 1)
# H = cv2.imread('../app/data/di-3^4-white-specular/H.png', 1)
# V = cv2.imread('../app/data/di-3^4-white-specular/V.png', 1)
H = cv2.imread('../app/data/red-oak-3-white-diffuse-1wk/H.png', 1)
V = cv2.imread('../app/data/red-oak-3-white-diffuse-1wk/V.png', 1)
P = cv2.imread('../app/data/red-oak-3-white-diffuse-1wk/P.png', 1)
M = cv2.imread('../app/data/red-oak-3-white-diffuse-1wk/M.png', 1)

H_grey = cv2.imread('../app/data/red-oak-3-white-diffuse-1wk/H.png', 0)
V_grey = cv2.imread('../app/data/red-oak-3-white-diffuse-1wk/V.png', 0)
P_grey = cv2.imread('../app/data/red-oak-3-white-diffuse-1wk/P.png', 0)
M_grey = cv2.imread('../app/data/red-oak-3-white-diffuse-1wk/M.png', 0)

indexes = np.where(H_grey != 0)
# indexes = np.where(H_grey != 0)
# for index, pixels in enumerate(zip(H, V)):
#     if pixels[0] == 0 or pixels[1] == 0:
#         indexes.append(index)
#
# print indexes

print H.shape
Hb, Hg, Hr = cv2.split(H)
Vb, Vg, Vr = cv2.split(V)
Pb, Pg, Pr = cv2.split(P)
Mb, Mg, Mr = cv2.split(M)


S1 = calculate_stokes(H, V)
S2 = calculate_stokes(P, M)

S1b = calculate_stokes(Hb, Vb)
S1g = calculate_stokes(Hg, Vg)
S1r = calculate_stokes(Hr, Vr)

S2b = calculate_stokes(Pb, Mb)
S2g = calculate_stokes(Pg, Mg)
S2r = calculate_stokes(Pr, Mr)

print '#####################'
img = np.array(np.abs(np.dstack((S1b, S1g, S1r))))
print img

# cv2.imshow('S1', np.abs(S1))
# # cv2.imwrite('img.png', img * 255)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.waitKey(1)


print H[indexes]

b_index = np.where(Hb != 0)
g_index = np.where(Hg != 0)
r_index = np.where(Hr != 0)

b_index2 = np.where(Pb != 0)
g_index2 = np.where(Pg != 0)
r_index2 = np.where(Pr != 0)

S1_hist = S1
S1b_hist = S1b
S1g_hist = S1g
S1r_hist = S1r

print S1b
plt.hist(S1_hist.ravel(), bins=np.linspace(-1,1,200))
plt.show()
plt.hist(S1b_hist.ravel(), bins=np.linspace(-1,1,200))
plt.show()
plt.hist(S1g_hist.ravel(), bins=np.linspace(-1,1,200))
plt.show()
plt.hist(S1r_hist.ravel(), bins=np.linspace(-1,1,200))
plt.show()


plt.hist(S2.ravel(), bins=np.linspace(-1,1,200))
plt.show()
plt.hist(S2b.ravel(), bins=np.linspace(-1,1,200))
plt.show()
plt.hist(S2g.ravel(), bins=np.linspace(-1,1,200))
plt.show()
plt.hist(S2r.ravel(), bins=np.linspace(-1,1,200))
plt.show()


S1_normed = np.power(S1,2)
S1_b_normed = np.sqrt(np.power(S1b,2) + np.power(S2b,2))
S1_g_normed = np.sqrt(np.power(S1g,2) + np.power(S2g,2))
S1_r_normed = np.sqrt(np.power(S1r,2) + np.power(S2r,2))
print S1_normed.astype(np.int8)

# cv2.imshow('S1', S1_normed)
cv2.imshow("S1b", S1_b_normed)
cv2.imshow("S1g", S1_g_normed)
cv2.imshow("S1r", S1_r_normed)

cv2.waitKey(0)
cv2.destroyAllWindows()
