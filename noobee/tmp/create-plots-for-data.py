from __future__ import division
import numpy as np

import cv2
import os
import matplotlib.pyplot as plt

def normed(data):
    print "data", data
    minimum = np.min(data)
    maximum = np.max(data)
    print "Maximum", maximum
    print "Minimum", minimum

    normed = (data - minimum) / (maximum - minimum)

    print "Normded", normed

    return normed

def calculate_stokes((S1, S2)):
    S1 = S1.astype(np.float32)
    S2 = S2.astype(np.float32)
    print "S1", S1
    print "S2", S2
    S1[np.abs(S1) < 1] = 0
    S2[np.abs(S2) < 1] = 0

    S = (S1 - S2) / (S1 + S2)

    # These represent values that have not been illuminated by the source
    # ie they are the product of masking and shadowing.
    S[~np.isfinite(S)] = 0

    return S

def createhistogram(raw_data, bins):
    data = raw_data.ravel()
    # bins = np.arange(np.floor(data.min()),np.ceil(data.max()))
    hist = np.histogram(data, bins=bins)
    bins = bins.tolist()
    # / len(data) to normalize to 1
    values = hist[0] / len(data)

    # Convert the tuples into arrays for smaller formatting
    zipped = [list(t) for t in zip(bins, values.tolist())]

    return zipped

def generate_stokes_total_histograms(img_dirs):
    H, V, P, M = [cv2.imread(os.path.join(img_dir, filter_angle_img), 1) for filter_angle_img in ['H.png', 'V.png', 'P.png', 'M.png']]

    S1 = calculate_stokes((H, V))
    S2 = calculate_stokes((P, M))
    print "S1max ", np.max(S1)
    print "S2max", np.max(S2)

    # plt.scatter(S1.ravel(), S2.ravel())
    # plt.show()
    # S1_hist = createhistogram(S1, [-1,-0.5,0.5,1])
    # S2_hist = createhistogram(S2, [-1,-0.5,0.5,1])
    # print S1_hist

    cv2.imwrite('S1.png', normed(S1) * 255)
    cv2.imwrite('S2.png', normed(S2) * 255)

    plt.title('Polarizance Paramaters')

    plt.hist(S1.ravel(),histtype='barstacked', bins=256)
    plt.hist(S2.ravel(),histtype='barstacked', bins=256)

    plt.show()


def generate_stokes_bgr_histograms(img_dirs, labels):
    plt.figure(1)
    plt.tick_params(labelsize=18)
    colors = ["#adadad", "#808080", "#5d5d5d"]

    for index, img_dir in enumerate(img_dirs):
        # H, V, P, M = [cv2.imread(os.path.join(img_dir, filter_angle_img), 1) for filter_angle_img in ['H.png', 'V.png', 'P.png', 'M.png']]

        H = cv2.imread(os.path.join(img_dir, 'H.png'), 1)
        V = cv2.imread(os.path.join(img_dir, 'V.png'), 1)
        P = cv2.imread(os.path.join(img_dir, 'P.png'), 1)
        M = cv2.imread(os.path.join(img_dir, 'M.png'), 1)


        # do individual channels
        H_b, H_g, H_r = cv2.split(H)
        V_b, V_g, V_r = cv2.split(V)
        P_b, P_g, P_r = cv2.split(P)
        M_b, M_g, M_r = cv2.split(M)


        S1 = calculate_stokes((H, V))
        S2 = calculate_stokes((P, M))
        # cv2.imwrite(os.path.join(img_dir, 'S1.png'), normed(S1) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'S2.png'), normed(S2) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'H_b.png'), normed(H_b) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'H_g.png'), normed(H_g) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'H_r.png'), normed(H_r) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'V_b.png'), normed(V_b) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'V_g.png'), normed(V_g) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'V_r.png'), normed(V_r) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'P_b.png'), normed(P_b) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'P_g.png'), normed(P_g) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'P_r.png'), normed(P_r) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'M_b.png'), normed(M_b) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'M_g.png'), normed(M_g) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'M_r.png'), normed(M_r) * 255)


        S1_b = calculate_stokes((H_b, V_b))
        S1_g = calculate_stokes((H_g, V_g))
        S1_r = calculate_stokes((H_r, V_r))

        S2_b = calculate_stokes((P_b, M_b))
        S2_g = calculate_stokes((P_g, M_g))
        S2_r = calculate_stokes((P_r, M_r))

        # cv2.imwrite(os.path.join(img_dir, 'S1_b.png'), normed(S1_b) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'S1_g.png'), normed(S1_g) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'S1_r.png'), normed(S1_r) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'S2_b.png'), normed(S2_b) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'S2_g.png'), normed(S2_g) * 255)
        # cv2.imwrite(os.path.join(img_dir, 'S2_r.png'), normed(S2_r) * 255)

        b_index = np.where(((H_b == 0) & (V_b == 0)) | ((P_b == 0) & (M_b == 0)))
        g_index = np.where((H_g == 0) & (V_g == 0))
        r_index = np.where((H_r == 0) & (V_r == 0))

        b_index2 = np.where(P_b != 0)
        g_index2 = np.where(P_g != 0)
        r_index2 = np.where(P_r != 0)

        # S1_hist = S1[indexes]
        print "LENGTH", len(S1)
        # S1 = S1[~(((H == 0) & (V == 0)) | ((P == 0) & (M == 0)))]
        # S2 = S2[~(((P == 0) & (M == 0)) | ((H == 0) & (V == 0)))]
        #
        # S1_b = S1_b[~(((H_b == 0) & (V_b == 0)) | ((P_b == 0) & (M_b == 0)))]
        # S1_g = S1_g[~(((H_g == 0) & (V_g == 0)) | ((P_g == 0) & (M_g == 0)))]
        # S1_r = S1_r[~(((H_r == 0) & (V_r == 0)) | ((P_r == 0) & (M_r == 0)))]
        #
        # S2_b = S2_b[~(((P_b == 0) & (M_b == 0)) | ((H_b == 0) & (V_b == 0)))]
        # S2_g = S2_g[~(((P_g == 0) & (M_g == 0)) | ((H_g == 0) & (V_g == 0)))]
        # S2_r = S2_r[~(((P_r == 0) & (M_r == 0)) | ((H_r == 0) & (V_r == 0)))]


        S1 = S1[~((H == 0) | (V == 0))]
        S2 = S2[~((P == 0) | (M == 0))]

        S1_b = S1_b[~((H_b == 0) | (V_b == 0))]
        S1_g = S1_g[~((H_g == 0) | (V_g == 0))]
        S1_r = S1_r[~((H_r == 0) | (V_r == 0))]

        S2_b = S2_b[~((P_b == 0) | (M_b == 0))]
        S2_g = S2_g[~((P_g == 0) | (M_g == 0))]
        S2_r = S2_r[~((P_r == 0) | (M_r == 0))]

        S1_weights = np.ones_like(S1)/float(len(S1))
        S1_b_weights = np.ones_like(S1_b)/float(len(S1_b))
        S1_g_weights = np.ones_like(S1_g)/float(len(S1_g))
        S1_r_weights = np.ones_like(S1_r)/float(len(S1_r))

        S2_weights = np.ones_like(S2)/float(len(S2))
        S2_b_weights = np.ones_like(S2_b)/float(len(S2_b))
        S2_g_weights = np.ones_like(S2_g)/float(len(S2_g))
        S2_r_weights = np.ones_like(S2_r)/float(len(S2_r))


        plt.figure(1)
        plt.tick_params(labelsize=18)
        plt.suptitle('S1 Polarization', fontsize=24)
        plt.subplot(221)

        plt.xticks(fontsize=16)
        # plt.xlabel('Polarization Intensity', fontsize=20)
        plt.xticks(fontsize=16)
        plt.ylabel('Normalized Frequency', fontsize=20)
        plt.yticks(fontsize=16)
        plt.title('RGB', fontsize=24)
        plt.hist(S1.ravel(),histtype='barstacked',weights=S1_weights, bins=256,color=colors[index], lw=0, alpha=0.6,label='%s \n (mean = %0.2f +/- %0.2f)' % (labels[index], np.mean(S1.ravel()), np.std(S1.ravel())))
        plt.legend(loc=2, fontsize=16)
        plt.subplot(222)

        # plt.xlabel('Polarization Intensity', fontsize=20)
        plt.xticks(fontsize=16)
        plt.ylabel('Normalized Frequency', fontsize=20)
        plt.yticks(fontsize=16)
        plt.title('Blue Channel', fontsize=24)
        plt.hist(S1_b.ravel(),histtype='barstacked',weights=S1_b_weights, bins=256,color=colors[index], lw=0, alpha=0.6, label='%s \n (mean = %0.2f +/- %0.2f)' % (labels[index], np.mean(S1_b.ravel()), np.std(S1_b.ravel())))
        plt.legend(loc=2, fontsize=16)
        plt.subplot(223)

        plt.xlabel('Polarization Intensity', fontsize=20)
        plt.xticks(fontsize=16)
        plt.ylabel('Normalized Frequency', fontsize=20)
        plt.yticks(fontsize=16)
        plt.title('Green Channel', fontsize=24)
        plt.hist(S1_g.ravel(),histtype='barstacked',weights=S1_g_weights, bins=256,color=colors[index], lw=0, alpha=0.6, label='%s \n (mean = %0.2f +/- %0.2f)' % (labels[index], np.mean(S1_g.ravel()), np.std(S1_g.ravel())))
        plt.legend(loc=2, fontsize=16)
        plt.subplot(224)

        plt.xlabel('Polarization Intensity', fontsize=20)
        plt.xticks(fontsize=16)
        plt.ylabel('Normalized Frequency', fontsize=20)
        plt.yticks(fontsize=16)
        plt.title('Red Channel', fontsize=24)
        plt.hist(S1_r.ravel(),histtype='barstacked', weights=S1_r_weights, bins=256,color=colors[index], lw=0, alpha=0.6, label='%s \n (mean = %0.2f +/- %0.2f)' % (labels[index], np.mean(S1_r.ravel()), np.std(S1_r.ravel())))
        plt.legend(loc=2, fontsize=16)

        plt.figure(2)
        plt.suptitle('S2 Polarization', fontsize=24)
        plt.subplot(221)

        plt.title('RGB',fontsize=24)
        # plt.xlabel('Polarization Intensity', fontsize=20)
        plt.xticks(fontsize=16)
        plt.ylabel('Normalized Frequency', fontsize=20)
        plt.yticks(fontsize=16)
        plt.hist(S2.ravel(),histtype='barstacked', weights=S2_weights, bins=256,color=colors[index], lw=0, alpha=0.6, label='%s \n (mean = %0.2f +/- %0.2f)' % (labels[index], np.mean(S2.ravel()), np.std(S2.ravel())))
        plt.legend(loc=2, fontsize=16)
        plt.subplot(222)

        # plt.xlabel('Polarization Intensity', fontsize=20)
        plt.xticks(fontsize=16)
        plt.ylabel('Normalized Frequency', fontsize=20)
        plt.yticks(fontsize=16)
        plt.title('Blue Channel',fontsize=24)
        plt.hist(S2_b.ravel(),histtype='barstacked', weights=S2_b_weights, bins=256,color=colors[index], lw=0, alpha=0.6, label='%s \n (mean = %0.2f +/- %0.2f)' % (labels[index], np.mean(S2_b.ravel()), np.std(S2_b.ravel())))
        plt.legend(loc=2, fontsize=16)
        plt.subplot(223)

        plt.xlabel('Polarization Intensity', fontsize=20)
        plt.xticks(fontsize=16)
        plt.ylabel('Normalized Frequency', fontsize=20)
        plt.yticks(fontsize=16)
        plt.title('Green Channel',fontsize=24)
        plt.hist(S2_g.ravel(),histtype='barstacked', weights=S2_g_weights, bins=256,color=colors[index], lw=0, alpha=0.6, label='%s \n (mean = %0.2f +/- %0.2f)' % (labels[index], np.mean(S2_g.ravel()), np.std(S2_g.ravel())))
        plt.legend(loc=2, fontsize=16)
        plt.subplot(224)

        plt.xlabel('Polarization Intensity', fontsize=20)
        plt.xticks(fontsize=16)
        plt.ylabel('Normalized Frequency', fontsize=20)
        plt.yticks(fontsize=16)
        plt.title('Red Channel', fontsize=24)
        plt.hist(S2_r.ravel(),histtype='barstacked', weights=S2_r_weights, bins=256,color=colors[index], lw=0, alpha=0.6, label='%s \n (mean = %0.2f +/- %0.2f)' % (labels[index], np.mean(S2_r.ravel()), np.std(S2_r.ravel())))
        plt.legend(loc=2, fontsize=16)

    plt.show()

######## offical diffuse #############
# labels = ['American Ash', 'Sugar Maple',  'Red Oak', ]
# img_dirs = ['../../app/data/american-ash-2-white-diffuse', '../../app/data/sugar-maple-2-white-diffuse', '../../app/data/red-oak-3-white-diffuse' ]
#######################################
# labels = ['American Ash 0wk', 'Americazn Ash 1wk' ]

#This is the current diffuse 0 1 wk
# labels = ['Sugar Maple 0wk', 'Sugar Maple 1wk' ]
# img_dirs = ['../../app/data/sugar-maple-2-white-diffuse', '../../app/data/sugar-maple-2-white-diffuse-1wk' ]
####
#
# labels = ['Sugar Maple 0wk', 'Sugar Maple 1wk' ]
# img_dirs = ['../../app/data/red-oak-2-white-diffuse', '../../app/data/red-oak-3-white-diffuse-1wk' ]



# labels = ['Red Oak 0wk', 'Red Oak 1wk' ]
# img_dirs = ['../../app/data/red-oak-2-white-specular', '../../app/data/red-oak-2-white-specular-1wk' ]

labels = ['Red Oak 0wk', 'Red Oak 1wk' ]
img_dirs = ['../../app/data/red-oak-1-white-diffuse', '../../app/data/red-oak-1-white-diffuse-1wk' ]



# for all 0 wk
# labels = ['American Ash 1', 'American Ash 2', 'American Ash 3', 'Sugar Maple 1', 'Sugar Maple 2','Sugar Maple 3', 'Red Oak 1', 'Red Oak 2', 'Red Oak 3']
# img_dirs = ['../../app/data/american-ash-1-white-specular','../../app/data/american-ash-2-white-specular', '../../app/data/american-ash-3-white-specular', '../../app/data/sugar-maple-1-white-specular','../../app/data/sugar-maple-2-white-specular','../../app/data/sugar-maple-3-white-specular', '../../app/data/red-oak-1-white-specular', '../../app/data/red-oak-2-white-specular', '../../app/data/red-oak-3-white-specular']


# labels = ['American Ash 0wk', 'American Ash 1wk', 'Sugar Maple 0wk', 'Sugar Maple 1wk', 'Red Oak 0wk', 'Red Oak 1wk']
# img_dirs = ['../../app/data/american-ash-2-white-specular','../../app/data/american-ash-1-white-specular-1wk', '../../app/data/sugar-maple-1-white-specular','../../app/data/sugar-maple-1-white-specular-1wk', '../../app/data/red-oak-1-white-specular', '../../app/data/red-oak-3-white-specular-1wk']



# labels = ['DI - 98 %', 'DI - 95%']
# img_dirs = ['../../app/data/di-3&3-white-diffuse','../../app/data/di-3&2-white-diffuse']




#
# labels = ['Devils Ivy']
# img_dirs = ['../../app/data/di-3^2-white-diffuse']

# labels = ['80 Grit', '100 Grit', '150 grit', '220 grit']
# img_dirs = ['../../app/data/grit-80-sandpaper-specular', '../../app/data/grit-100-sandpaper-specular', '../../app/data/grit-150-sandpaper-specular', '../../app/data/grit-220-sandpaper-specular']
#
# labels = ['100 Grit', '220 grit']
# #
# img_dirs = ['../../app/data/grit-100-sandpaper-specular', '../../app/data/grit-220-sandpaper-specular']


generate_stokes_bgr_histograms(img_dirs, labels)
