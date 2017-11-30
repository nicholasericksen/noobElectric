from __future__ import division
import numpy as np
from sklearn import svm, linear_model
from sklearn.decomposition import PCA as sklearnPCA
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score

# data = np.genfromtxt('rwc-raw.csv', skip_header=1, delimiter=',')
# y = [data[0] for data in data]
# print "Y", len(y)
# X = [np.delete(data, 0) for data in data]
# X = data
# print len(X)
X_unnormed = np.genfromtxt('rwc-raw.csv', delimiter=',', usecols=(range(1,598)), skip_header=1)
y = np.genfromtxt('rwc-raw.csv', delimiter=',', usecols=(0), skip_header=1)


X = (X_unnormed - X_unnormed.min())/(X_unnormed.max() - X_unnormed.min())

# X = [[1,1,1],[2,2,2], [3,3,3], [4,4,4],[5,5,5], [6,6,6], [7,7,7], [8,8,8], [9,9,9]]
# y=[1,2,3,4,5,6,7,8,9]

# X = [[1,1], [3,3]]
# y = [1, 3]

clf = svm.SVR(C=1e9)

scores = cross_val_score(clf, X, y, cv=2)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


fit = clf.fit(X, y)
fit_y = fit.predict(X)

pca = sklearnPCA(n_components=1)
trans = pca.fit_transform(X)
X_trans = trans[:, 0]

print "X_trans", X_trans
print "fit_y", fit_y

regr = linear_model.LinearRegression()
regr.fit(X, y)
y2 = regr.predict(X)

plt.scatter(X_trans, y)
plt.plot(X_trans, fit_y)

plt.show()
