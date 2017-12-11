from __future__ import division
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import svm, linear_model
from sklearn.decomposition import PCA as sklearnPCA
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, explained_variance_score, mean_squared_error
from sklearn.preprocessing import label_binarize, scale, normalize
# data = np.genfromtxt('rwc-raw.csv', skip_header=1, delimiter=',')
# y = [data[0] for data in data]
# print "Y", len(y)
# X = [np.delete(data, 0) for data in data]
# X = data
# print len(X)
# rwc-specular is a measure of 50 75px x 75 px samples of each leaf
data = np.genfromtxt('rwc-specular-all-less-rwc-precision-75.csv', delimiter=',')
X = data[:,1:]
X = normalize(X)
y = data[:,0]


# X = (X_unnormed - X_unnormed.min())/(X_unnormed.max() - X_unnormed.min())
# print X
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# X = [[1,1,1],[2,2,2], [3,3,3], [4,4,4],[5,5,5], [6,6,6], [7,7,7], [8,8,8], [9,9,9]]
# y=[1,2,3,4,5,6,7,8,9]

# X = [[3,3],[1,1.5], [4,4.3], [5,5]]
# y = [3,1,4,5]

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)

# tuned_parameters = [{'kernel': ['linear'], 'C': [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,2,3,4,5,6, 10, 100], 'epsilon': [1e-1, .3,.4,.5,.7,.6,.9]}]
# #
# clfer = GridSearchCV(svm.SVR(), tuned_parameters, cv=5)
# clfer.fit(X_train, y_train)
# print "clf score: ", clfer.score(X_test, y_test)
# print("Best parameters set found on development set:")
# print()
# print(clfer.best_params_)

#(3, .5) (.5, .01) (1, .5) (2, .6) (.6, .08)

clf = svm.SVR(kernel='sigmoid', C=10, epsilon=.0001)
pca = sklearnPCA(n_components=2)
trans = pca.fit_transform(X)
X_trans = trans[:, 0]
print "x-trans", X_trans
fit = clf.fit(X_train, y_train)
fit_y = fit.predict(X)
print "score: ", fit.score(X_test, y_test)
print "r2: ", r2_score(y, fit_y, multioutput='variance_weighted')
print "explained_variance_score: ", explained_variance_score(y, fit_y)
print "root mean squared: ", mean_squared_error(y, fit_y)
scores = cross_val_score(clf, X_train, y_train, cv=5)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


# print "trans", trans

# print "X_trans", X_trans
# print "fit_y", fit_y
# X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(X_trans, y, test_size=0.5, random_state=0)
#
# print "X_train_2", X_train_2.shape
# print "Ytrain2", y_train_2.shape
# regr = linear_model.LinearRegression()
# regr.fit([X_train_2], y_train_2)
# print X_test_2.shape
# y2 = regr.predict([X_test_2])


# Train e model using the training sets
# regr.fit(X_train, y_train)
# Make predictions using the testing set
# y_pred = regr.predict(X_test[:,0])
# print "HAHAHA",  y_pred
#
#
# plt.scatter(X_test_2, y_test_2)
# plt.plot(X_test_2, y2)
# plt.show()







plt.scatter(X_trans, y, s=30, label='data')
plt.scatter(X_trans, fit_y, marker='x', s=30, label='model', color='r')



# X_trans, fit_y = zip(*sorted(zip(X_trans,fit_y)))

p = X_trans.argsort()
plt.plot(X_trans[p].reshape(-1, 1), fit_y[p])
plt.title('Relative Water Content (RWC)')
plt.xlabel('First Principal Component')
plt.ylabel('RWC (%)')
plt.legend(loc='best')
plt.show()
