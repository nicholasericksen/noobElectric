import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

pathname = os.path.join(os.getcwd(), "raw_data", "imgs")

H_raw = cv2.imread(os.path.join(pathname, "H.png"), 0)
V_raw = cv2.imread(os.path.join(pathname, "V.png"), 0)

H = H_raw.ravel().astype(np.int16)
V = V_raw.ravel().astype(np.int16)
print(H.shape)
print (V.shape)
print (H)
#plt.hist(H, bins=255)
#plt.hist(V, bins=255)
#plt.show()

S1 = []
for px1, px2 in zip(H, V):
    denom = px1 + px2
    if denom == 0:
        continue
    #elif px1 == 0 or px2 == 0:
    #    continue
    #elif px1 > 250 or px2 > 250:
    #    continue
    else:
        S = (px1-px2) / (px1+px2)
        #S[~np.isfinite(S)] = 0
        S1.append(S)
S1 = np.array(S1)
print(S1)
print("MEAN: {}".format(S1.mean()))
print("STD: {}".format(S1.std()))
#print(S1)
plt.hist(S1, bins=255)
plt.show()
