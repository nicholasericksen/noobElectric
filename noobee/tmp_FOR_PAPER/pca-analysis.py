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

#########################
#Specular RWC samples
# (img)     1_1 -> 98.4379
# (img2)    31  -> 97.6573
# (img3)    3^4 -> 96.6949
# (imgs4)   2+1 -> 88.8809
# (imgs5)   2+2 -> 92.4017
# (imgs6)   3+1 -> 95.4651
#########################

directory = 'imgs4'
P1_img = 'H.png'
P2_img = 'V.png'

# we should ask for path name of directory and if not use the current one

#for img_file in os.listdir(pathname):
#    print img_file
#    if img_file == 'H.png':
#   
# input directory name and image name
# returns list of flux values for polarization filtered image
def img_to_flux(P_img_name):
    pathname = os.path.join(os.getcwd(), directory)
    P_raw = cv2.imread(os.path.join(pathname, P_img_name), 0)
    P = P_raw.ravel().astype(np.int16)
    return P

# input two arrays of flux values
# output numpy array of stokes values
def calc_stokes(P1, P2):
    S = []
    for P1_px,P2_px in zip(P1,P2):
        #denom = P1 + P2
        # Filter out if values never change from 0
        #if denom == 0:
        #    continue
        # Filter out if values are ever higher than 225
        if P1_px == 0 or P2_px == 0:
            continue
        elif P1_px > 225 or P2_px > 225:
            continue
    #    elif P1 < 25 or P2 < 25:
    #        continue
        else:
            calc = (P1_px - P2_px) / (P1_px + P2_px)
            S.append(calc)
    return np.array(S)

# Show image using CV2
def show_image(img):
    pathname = os.path.join(os.getcwd(), directory)
    image_path = os.path.join(pathname, img)
    raw_img = cv2.imread(image_path, 0)
    cv2.imshow('image', raw_img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #cv2.waitKey(1)
#H = [px for px in H if px < 225 and px != 0]

# TODO add printing yes no option
def stats_stokes(S):
    printer = True
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

    if show_images == True:
        show_image(P1_img)
        plot_histogram(img_to_flux(P1_img))
        show_image(P2_img)
        plot_histogram(img_to_flux(P1_img))
    if plot_hist == True:
        plot_histogram(S)
    if calc_stats == True:
        stats = stats_stokes(S)
        return S, stats
    else:
        return S

S, stats = stokes_analysis(P1_img, P2_img)
print(stats)
#####################
## RWC Plotting   ##
#####################
# Plot a couple RWCs against S1 polarization mean and std
# X is now X_stds since its results were more promising
X = [0.4278,0.3074, 0.3332, 0.5124, 0.4721, 0.4320]
X_means = [-0.2640, -0.1660, 0.1327, -0.04508, 0.1063, 0.1080]
y = [98.4379, 97.6573, 96.6949, 88.8809, 92.4017, 95.4651]
plt.scatter(X, y)
plt.show()

#######################
## Linear regression ##
#######################
#reshape since it is only one feature at the moment
X = np.array(X)
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
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

plt.title('Linear Regression For Relative Water Content')
plt.xlabel('First Principal Component')
plt.ylabel('Relative Water Content')
plt.scatter(X[:,0], y)
plt.plot(X[:,0].reshape(-1, 1), y_pred)

plt.show()
####################
####################
