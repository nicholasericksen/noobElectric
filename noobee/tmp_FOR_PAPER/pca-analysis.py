from __future__ import division
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


######################
# Regression imports #
from sklearn import linear_model
from sklearn.metrics import r2_score, explained_variance_score, mean_squared_error
from sklearn.model_selection import train_test_split, cross_val_score
######################

###### PCA IMports #####
from sklearn.decomposition import PCA as sklearnPCA

#########################
#Specular RWC samples
# (imgs)     1_1 -> 98.4379
# (imgs2)    31  -> 97.6573
# (imgs3)    3^4 -> 96.6949
# (imgs4)   2+1 -> 88.8809
# (imgs5)   2+2 -> 92.4017
# (imgs6)   3+1 -> 95.4651
#########################


# we should ask for path name of directory and if not use the current one

#for img_file in os.listdir(pathname):
#    print img_file
#    if img_file == 'H.png':
#   
# input directory name and image name
# returns list of flux values for polarization filtered image
def img_to_flux(P_img):
    P = P_img.ravel().astype(np.int16)
    return P

# input two arrays of flux values
# output numpy array of stokes values
def calc_stokes(P1, P2):
    S = []
    for P1_px,P2_px in zip(P1,P2):
        denom = P1_px + P2_px
        # Filter out if values never change from 0
        if denom == 0:
            continue
        # Filter out if values are ever higher than 225
        if P1_px < 10 or P2_px < 10:
            continue
        elif P1_px > 245 or P2_px > 245:
            continue
    #    elif P1 < 25 or P2 < 25:
    #        continue
        else:
            calc = (P1_px - P2_px) / (P1_px + P2_px)
            S.append(calc)
    return np.array(S)

# Show image using CV2
def show_image(img):
    image_path = os.path.join(pathname, img)
    raw_img = cv2.imread(image_path, 0)
    cv2.imshow('image', raw_img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #cv2.waitKey(1)
#H = [px for px in H if px < 225 and px != 0]

# TODO add printing yes no option
def stats_stokes(S):
    printer = False
    maximum = max(S)
    minimum = min(S)
    mean = S.mean()
    std = S.std()

    if printer == True:
        print("MAX: ", maximum)
        print("MIN: ", minimum)
        print("MEAN: ", mean)
        print("STD: ", std)

    stats = {}
    stats["mean"] = mean
    stats["std"] = std
    stats["min"] = minimum
    stats["max"] = maximum
    return stats

def plot_histogram(S):
    plt.hist(S, bins=255)
    plt.show()

def stokes_analysis(P1_img, P2_img):
    # Options
    show_images = False
    calc_stats = True
    plot_hist = True

    # Convert image pixel intensity to flux values
    P1 = img_to_flux(P1_img)
    P2 = img_to_flux(P2_img)

    # Calculate the Stokes parameter
    S = calc_stokes(P1, P2)
    print(S)
    results = {}
    results["S"] = S

    if show_images == True:
        show_image(P1_img)
        plot_histogram(img_to_flux(P1_img))
        show_image(P2_img)
        plot_histogram(img_to_flux(P1_img))
    if plot_hist == True:
        plot_histogram(S)
    if calc_stats == True:
        stats = stats_stokes(S)
        results["stats"] = stats
    return results
#####################
## RWC Plotting   ##
#####################
# Plot a couple RWCs against S1 polarization mean and std
# X is now X_stds since its results were more promising
X = [0.4278,0.3074, 0.3332, 0.5124, 0.4721, 0.4320]
X_means = [-0.2640, -0.1660, 0.1327, -0.04508, 0.1063, 0.1080]
y = [98.4379, 97.6573, 96.6949, 88.8809, 92.4017, 95.4651]
#plt.scatter(X, y)
#plt.show()

#######################
## Linear regression ##
#######################
# Question: how do we group X and y
def read_dat_file(pathname):
    data = []
    with open(pathname) as dat_file:
        for value in dat_file:
            data.append(value.rstrip('\n'))
    return float(data[0])
#reshape since it is only one feature at the moment
def linear_analysis(X, y):

    X = np.array(X)
#    y = np.array(y)
    X = X.reshape(-1,1)
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)
    regr = linear_model.LinearRegression()
    regr.fit(X, y)

    # X_axis = np.linspace(0,100,1).T
    y_pred = regr.predict(X)

    # Calculate and print classifier metrics
    print("r2: ", r2_score(y, y_pred, multioutput='variance_weighted'))
    print("explained_variance_score: ", explained_variance_score(y, y_pred))
    print("root mean squared: ", mean_squared_error(y, y_pred))
    scores = cross_val_score(regr, X, y, cv=2)
    print("Accurcy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    plt.title('Linear Regression For Relative Water Content')
    plt.xlabel('First Principal Component')
    plt.ylabel('Relative Water Content')
    plt.scatter(X[:,0], y)
    plt.plot(X[:,0].reshape(-1, 1), y_pred)

    plt.show()
####################
####################
def main():
    raw_data_path = os.path.join(os.getcwd(), "raw_data")
    raw_data = os.listdir(raw_data_path)
    datasets  = [f for f in raw_data if not f.startswith('.')]
    #print(datasets)
    #print(raw_data_path)
    P1_img_name = 'H.png'
    P2_img_name = 'V.png'

    X = []
    y = []

    for directory in datasets:
        pathname = os.path.join(raw_data_path, directory)

        # Stokes analysis
        P1_img = cv2.imread(os.path.join(pathname, P1_img_name), 1)
        P2_img = cv2.imread(os.path.join(pathname, P2_img_name), 1)
        data = stokes_analysis(P1_img[0], P2_img[0])

        # RWC Infromation
        dat_file_path = os.path.join(pathname, "rwc.dat")
        data["rwc"] = read_dat_file(dat_file_path)
        #print(data["stats"])
        #print("RWC: {}".format(data["rwc"]))
        X.append(data["stats"]["std"])
        y.append(data["rwc"])
    # Linear Regression
    print("X: {}".format(X))
    print("y: {}".format(y))
    pca = sklearnPCA(n_components=1)
    X = pca.fit_transform(X)
    linear_analysis(X,y)

if __name__ ==  '__main__':
    main()
