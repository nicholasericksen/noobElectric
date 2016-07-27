import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

from skimage.filters import threshold_otsu

imgs = [
    {'name': 'imgs/10um.jpg', 'title': 'Tumor at 10um'},
    {'name': 'imgs/30um.jpg', 'title': 'Tumor at 30um'},
    {'name': 'imgs/40um.jpg', 'title': 'Tumor at 40um'},
    {'name': 'imgs/60um.jpg', 'title': 'Tumor at 60um'},
    {'name': 'imgs/100um.jpg', 'title': 'Tumor at 100um'},
    {'name': 'imgs/110um.jpg', 'title': 'Tumor at 110um'},
    {'name': 'imgs/120um.jpg', 'title': 'Tumor at 120um'},
    {'name': 'imgs/140um.jpg', 'title': 'Tumor at 140um'},
    {'name': 'imgs/160um.jpg', 'title': 'Tumor at 160um'}
]


def processImg(img, title):
        plt.subplot(221)
        plt.imshow(img)
        plt.title(title)
        plt.xlabel('X-Coordinate', fontsize=10)
        plt.ylabel('Y-Coordinate', fontsize=10)

        plt.subplot(222)
        plt.hist(img.ravel())
        plt.title('Histogram ' + title)
        plt.xlabel('Pixel Intensity', fontsize=10)
        plt.ylabel('Frequency', fontsize=10)

def processOtsuImg(img, title):
        threshold = threshold_otsu(img)
        print(threshold)
        binary = img >= threshold

        plt.subplot(223)
        plt.imshow(binary)
        plt.title('Outsu ' + title)
        plt.xlabel('X-Coordinate', fontsize=10)
        plt.ylabel('Y-Coordinate', fontsize=10)

        plt.subplot(224)
        plt.hist(binary.ravel())
        plt.title('Outsu Histogram ' + title)
        plt.xlabel('Pixel Intensity', fontsize=10)
        plt.ylabel('Frequency', fontsize=10)

for img in imgs:
        image = mpimg.imread(str(img['name']))
        title = str(img['title'])
        processImg(image, title)
        processOtsuImg(image, title)
        plt.tight_layout()
        plt.show()
