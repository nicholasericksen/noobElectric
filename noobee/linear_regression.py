from __future__ import division
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import linear_model
from sklearn.decomposition import PCA as sklearnPCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, explained_variance_score, mean_squared_error
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import PolynomialFeatures
# data = np.genfromtxt('rwc-raw.csv', skip_header=1, delimiter=',')
# y = [data[0] for data in data]
# print "Y", len(y)
# X = [np.delete(data, 0) for data in data]
# X = data
# print len(X)
# rwc-specular is a measure of 50 75px x 75 px samples of each leaf
transformer = FunctionTransformer(np.log1p)
data = np.genfromtxt('TEST__rwc-specular-all-less-rwc-precision-75.csv', delimiter=',')
# data = np.genfromtxt('rwc-specular-all-less-rwc-precision-75.csv', delimiter=',')
X = data[:,1:]

# X = scale(X)
X = normalize(X, axis=1)
X = transformer.transform(X)
poly = PolynomialFeatures(degree=1)
X = poly.fit_transform(X)

y = data[:,0]

pca = sklearnPCA(n_components=1)
X = pca.fit_transform(X)

print X
mean = np.mean(X)
std = np.std(X)


# X = (X_unnormed - X_unnormed.min())/(X_unnormed.max() - X_unnormed.min())
# print X
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)
regr = linear_model.LinearRegression()
regr.fit(X, y)

# X_axis = np.linspace(0,100,1).T
y_pred = regr.predict(X)

print "r2: ", r2_score(y, y_pred, multioutput='variance_weighted')
print "explained_variance_score: ", explained_variance_score(y, y_pred)
print "root mean squared: ", mean_squared_error(y, y_pred)
scores = cross_val_score(regr, X, y, cv=10)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


plt.title('Linear Regression For Relative Water Content')
plt.xlabel('First Principal Component')
plt.ylabel('Relative Water Content')
plt.scatter(X[:,0], y)
plt.plot(X[:,0].reshape(-1, 1), y_pred)

plt.show()
