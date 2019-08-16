>>> from skimage.filters import threshold_otsu
>>> import matplotlib.pyplot as plt
>>> from __future__ import division
>>> import cv2
>>> import numpy as np
>>>
>>> image = cv2.imread('H.png', 1)
>>> b,g,r = cv2.split(image)
>>> b_thresh = threshold_otsu(b)
>>> b_binary = b > b_threshold
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'b_threshold' is not defined
>>> b_binary = b > b_thresh
>>> plt.show('b_binary', b_binary)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/ne/anaconda/lib/python2.7/site-packages/matplotlib/pyplot.py", line 244, in show
    return _show(*args, **kw)
TypeError: __call__() takes at most 2 arguments (3 given)
>>> cv2.imshow('b_binary', b_binary)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: mat data type = 0 is not supported
>>> cv2.imshow('b', b)
>>> cv2.destroyAllWindows()
>>> print b_thresh
139
>>> print b_binary
[[False False False ...,  True  True False]
 [False False False ...,  True False False]
 [False False False ..., False False False]
 ...,
 [False False False ..., False  True  True]
 [False False False ..., False False False]
 [False False False ..., False False False]]
>>> cv2.imshow('b_binary', b_binary)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: mat data type = 0 is not supported
>>> int(b_binary == 'true')
__main__:1: FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
0
>>> b_binary*1
array([[0, 0, 0, ..., 1, 1, 0],
       [0, 0, 0, ..., 1, 0, 0],
       [0, 0, 0, ..., 0, 0, 0],
       ...,
       [0, 0, 0, ..., 0, 1, 1],
       [0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0]])
>>> cv2.imshow(b_binary*1)

>>> img = b_binary*255
>>> img
array([[  0,   0,   0, ..., 255, 255,   0],
       [  0,   0,   0, ..., 255,   0,   0],
       [  0,   0,   0, ...,   0,   0,   0],
       ...,
       [  0,   0,   0, ...,   0, 255, 255],
       [  0,   0,   0, ...,   0,   0,   0],
       [  0,   0,   0, ...,   0,   0,   0]])
>>> cv2.imshow('img', img)
>>> cv2.destroyAllWindows()
>>> img = np.array(img, dtype=np.uint8)
>>> cv2.imshow('img', img)
>>> cv2.destroyAllWindows()
