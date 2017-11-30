from __future__ import division
import numpy as np

import cv2
import os
import matplotlib.pyplot as plt

def calculate_stokes((P1, P2)):
    P1 = P1.astype(np.int16)
    P2 = P2.astype(np.int16)

    S = (P1 - P2) / (P1 + P2)

    # These represent values that have not been illuminated by the source
    # ie they are the product of masking and shadowing.
    S[~np.isfinite(S)] = 0

    return S

def normed(data):
    minimum = np.min(data)
    maximum = np.max(data)

    normed = (data - minimum) / (maximum - minimum)

    return normed



def generate_stokes_total_histograms(img_dirs):
    H, V, P, M = [cv2.imread(os.path.join(img_dir, filter_angle_img), 1) for filter_angle_img in ['H.png', 'V.png', 'P.png', 'M.png']]

    S1 = calculate_stokes((H, V))
    S2 = calculate_stokes((P, M))
    print "S1max ", np.max(S1)
    print "S2max", np.max(S2)

    # plt.scatter(S1.ravel(), S2.ravel())
    # plt.show()
    # S1_hist = createhistogram(S1, np.linspace(-1, 1, 200))
    # S2_hist = createhistogram(S2, np.linspace(-1, 1, 200))
    # print S1_hist

    cv2.imwrite('S1.png', normed(S1) * 255)
    cv2.imwrite('S2.png', normed(S2) * 255)

    plt.title('Polarizance Paramaters')

    plt.hist(S1.ravel(), bins=np.linspace(-1, 1, 200), normed=True)
    plt.hist(S2.ravel(), bins=np.linspace(-1, 1, 200), normed=True)

    plt.show()


def generate_stokes_bgr_histograms(img_dirs, labels):
    plt.figure(1)
    for index, img_dir in enumerate(img_dirs):
        H, V, P, M = [cv2.imread(os.path.join(img_dir, filter_angle_img), 1) for filter_angle_img in ['H.png', 'V.png', 'P.png', 'M.png']]
        # do individual channels
        H_b, H_g, H_r = cv2.split(H)
        V_b, V_g, V_r = cv2.split(V)
        P_b, P_g, P_r = cv2.split(P)
        M_b, M_g, M_r = cv2.split(M)


        S1 = calculate_stokes((H, V))
        S2 = calculate_stokes((P, M))
        cv2.imwrite(os.path.join(img_dir, 'S1.png'), normed(S1) * 255)
        cv2.imwrite(os.path.join(img_dir, 'S2.png'), normed(S2) * 255)
        cv2.imwrite(os.path.join(img_dir, 'H_b.png'), normed(H_b) * 255)
        cv2.imwrite(os.path.join(img_dir, 'H_g.png'), normed(H_g) * 255)
        cv2.imwrite(os.path.join(img_dir, 'H_r.png'), normed(H_r) * 255)
        cv2.imwrite(os.path.join(img_dir, 'V_b.png'), normed(V_b) * 255)
        cv2.imwrite(os.path.join(img_dir, 'V_g.png'), normed(V_g) * 255)
        cv2.imwrite(os.path.join(img_dir, 'V_r.png'), normed(V_r) * 255)
        cv2.imwrite(os.path.join(img_dir, 'P_b.png'), normed(P_b) * 255)
        cv2.imwrite(os.path.join(img_dir, 'P_g.png'), normed(P_g) * 255)
        cv2.imwrite(os.path.join(img_dir, 'P_r.png'), normed(P_r) * 255)
        cv2.imwrite(os.path.join(img_dir, 'M_b.png'), normed(M_b) * 255)
        cv2.imwrite(os.path.join(img_dir, 'M_g.png'), normed(M_g) * 255)
        cv2.imwrite(os.path.join(img_dir, 'M_r.png'), normed(M_r) * 255)


        S1_b = calculate_stokes((H_b, V_b))
        S1_g = calculate_stokes((H_g, V_g))
        S1_r = calculate_stokes((H_r, V_r))

        S2_b = calculate_stokes((P_b, M_b))
        S2_g = calculate_stokes((P_g, M_g))
        S2_r = calculate_stokes((P_r, M_r))

        cv2.imwrite(os.path.join(img_dir, 'S1_b.png'), normed(S1_b) * 255)
        cv2.imwrite(os.path.join(img_dir, 'S1_g.png'), normed(S1_g) * 255)
        cv2.imwrite(os.path.join(img_dir, 'S1_r.png'), normed(S1_r) * 255)
        cv2.imwrite(os.path.join(img_dir, 'S2_b.png'), normed(S2_b) * 255)
        cv2.imwrite(os.path.join(img_dir, 'S2_g.png'), normed(S2_g) * 255)
        cv2.imwrite(os.path.join(img_dir, 'S2_r.png'), normed(S2_r) * 255)

        plt.figure(1)
        plt.suptitle('P1 Polarization', fontsize=20)
        plt.subplot(221)
        plt.xlabel('Polarization Intensity', fontsize=9)
        plt.ylabel('Normalized Frequency', fontsize=9)
        plt.title('RGB')
        plt.hist(S1.ravel(), bins=np.linspace(-1, 1, 200), normed=True, label=labels[index])
        plt.subplot(222)
        plt.xlabel('Polarization Intensity', fontsize=9)
        plt.ylabel('Normalized Frequency', fontsize=9)
        plt.title('Blue Channel')
        plt.hist(S1_b.ravel(), bins=np.linspace(-1, 1, 200), normed=True, label=labels[index])
        plt.subplot(223)
        plt.xlabel('Polarization Intensity', fontsize=9)
        plt.ylabel('Normalized Frequency', fontsize=9)
        plt.title('Green Channel')
        plt.hist(S1_g.ravel(), bins=np.linspace(-1, 1, 200), normed=True, label=labels[index])
        plt.subplot(224)
        plt.xlabel('Polarization Intensity', fontsize=9)
        plt.ylabel('Normalized Frequency', fontsize=9)
        plt.title('Red Channel')
        plt.hist(S1_r.ravel(), bins=np.linspace(-1, 1, 200), normed=True, label=labels[index])
        plt.legend()

        plt.figure(2)
        plt.suptitle('P2 Polarization', fontsize=20)
        plt.subplot(221)
        plt.title('RGB')
        plt.xlabel('Polarization Intensity', fontsize=9)
        plt.ylabel('Normalized Frequency', fontsize=9)
        plt.hist(S2.ravel(), bins=np.linspace(-1, 1, 200), normed=True, label=labels[index])
        plt.subplot(222)
        plt.xlabel('Polarization Intensity', fontsize=9)
        plt.ylabel('Normalized Frequency', fontsize=9)
        plt.title('Blue Channel')
        plt.hist(S2_b.ravel(), bins=np.linspace(-1, 1, 200), normed=True, label=labels[index])
        plt.subplot(223)
        plt.xlabel('Polarization Intensity', fontsize=9)
        plt.ylabel('Normalized Frequency', fontsize=9)
        plt.title('Green Channel')
        plt.hist(S2_g.ravel(), bins=np.linspace(-1, 1, 200), normed=True, label=labels[index])
        plt.subplot(224)
        plt.xlabel('Polarization Intensity', fontsize=9)
        plt.ylabel('Normalized Frequency', fontsize=9)
        plt.title('Red Channel')
        plt.hist(S2_r.ravel(), bins=np.linspace(-1, 1, 200), normed=True, label=labels[index])
        plt.legend()

    plt.show()

labels = ['American Ash', 'Sugar Maple', 'Red Oak']
img_dirs = ['../../app/data/american-ash-2-white-diffuse', '../../app/data/sugar-maple-1-white-diffuse', '../../app/data/red-oak-1-white-diffuse']

# labels = ['60 Grit', '100 Grit']
# img_dirs = ['../../app/data/sandpaper-brown-60-grit', '../../app/data/sandpaper-100-grit-brown-red-filter']
generate_stokes_bgr_histograms(img_dirs, labels)
