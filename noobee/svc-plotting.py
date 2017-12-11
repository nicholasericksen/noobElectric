from __future__ import division
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import svm
import numpy as np

from sklearn.metrics import roc_curve, auc
import itertools
from sklearn.preprocessing import label_binarize, scale, normalize
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.metrics import confusion_matrix, classification_report

from sklearn.decomposition import PCA as sklearnPCA

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


X = np.genfromtxt('specular-trees.csv', delimiter=',')
# X = scale(X)
X = normalize(X, axis=0)
# print X

ash_label = np.full((300,), 0)
oak_label = np.full((300,), 1)
maple_label = np.full((300,),2)

# grit_220 = np.full((100,), 3)
# grit_150 = np.full((100,), 2)
# grit_100 = np.full((100,), 1)
# grit_80 = np.full((100,), 0)

# print ash_label
y = np.concatenate((ash_label, oak_label, maple_label))
# y = np.concatenate((grit_80, grit_100, grit_150, grit_220))

# binarize the labels for roc_curve
# y = label_binarize(y, classes=[0,1,2])
# y = label_binarize(y, classes=[0,1])
# n_classes = y.shape[1]
# print "n", n_classes
# print y



# pca = sklearnPCA(n_components=2)
# X = pca.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=8)
print "X_train shape", X_train.shape

clf = svm.SVC(kernel='linear', C=1)
y_pred = clf.fit(X_train, y_train).predict(X_test)

cnf_matrix = confusion_matrix(y_test, y_pred)
print cnf_matrix
np.set_printoptions(precision=2)
print classification_report(y_test, y_pred)

class_names = ['ash', 'oak', 'maple']
# class_names = ['80 Grit', '100 Grit', '150 Grit', '220 Grit']
plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                      title='Normalized confusion matrix')
plt.show()
coef = clf.coef_
# print "coef", coef
print coef.shape

feature_labels = ['S1_b mean', 'S1_b std', 'S1_g mean', 'S1_g std', 'S1_r mean', 'S1_r std', 'S2_b mean', 'S2_b std', 'S2_g mean', 'S2_g std', 'S2_r mean', 'S2_r std', 'H_b diss','H_b contrast', 'H_b corr', 'H_b energy', 'H_g diss','H_g contrast', 'H_g corr', 'H_g energy', 'H_r diss','H_r contrast', 'H_r corr', 'H_r energy', 'V_b diss','V_b contrast', 'V_b corr', 'V_b energy', 'V_g diss','V_g contrast', 'V_g corr', 'V_g energy', 'V_r diss','V_r contrast', 'V_r corr', 'V_r energy',
'P_b diss','P_b contrast', 'P_b corr', 'P_b energy', 'P_g diss','P_g contrast', 'P_g corr', 'P_g energy', 'P_r diss','P_r contrast', 'P_r corr', 'P_r energy', 'M_b diss','M_b contrast', 'M_b corr', 'M_b energy', 'M_g diss','M_g contrast', 'M_g corr', 'M_g energy', 'M_r diss','M_r contrast', 'M_r corr', 'M_r energy']
X_bar = np.arange(0,coef.shape[1],1)
p = coef[0].argsort()

plt.bar(X_bar, coef[0], color='r')
# plt.xticks(X_bar, feature_labels, rotation=90)
plt.show()


h = .02
# plt.scatter(X[0:299,0], X[0:299,3])

print X
print "X shape", X.shape

x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
y_min, y_max = X[:, 1].min() - .5, X[:,1].max() + .5
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
# Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
#
# # Put the result into a color plot
# Z = Z.reshape(xx.shape)
# plt.figure(1, figsize=(4, 3))
# plt.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired)

# Plot also the training points
def plot_hyperplane(clf, min_x, max_x, linestyle, label):
    # get the separating hyperplane
    w = clf.coef_[0]
    a = -w[0] / w[1]
    xx = np.linspace(min_x - 5, max_x + 5)  # make sure the line is long enough
    yy = a * xx - (clf.intercept_[0]) / w[1]
    plt.plot(xx, yy, linestyle, label=label)




plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=80,
                facecolors='none', zorder=10, edgecolors='k')
# plt.scatter(X[:, 0], X[:, 1], c=['r','g','b'], zorder=10, cmap=plt.cm.Paired,
#                 edgecolors='k')
# x_min = -15
# x_max = 25
# y_min = -20
# y_max = 40
#
# XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
# Z = clf.decision_function(np.c_[XX.ravel(), YY.ravel()])
#
# # Put the result into a color plot
# Z = Z.reshape(XX.shape)
# plt.figure(fignum, figsize=(4, 3))
# plt.pcolormesh(XX, YY, Z > 0, cmap=plt.cm.Paired)
# plt.contour(XX, YY, Z, colors=['k', 'k', 'k'], linestyles=['--', '-', '--'],
#             levels=[-.5, 0, .5])

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
# plt.scatter(X[:, 0], X[:, 1], c=['r', 'g', 'b'], edgecolors='k', cmap=plt.cm.Paired)
# plt.xlabel('Sepal length')
# plt.ylabel('Sepal width')
#
# plot_hyperplane(clf.estimators_[0], x_min, x_max, 'k--', 'class 1')
#
# plt.xlim(xx.min(), xx.max())
# plt.ylim(yy.min(), yy.max())
# plt.xticks(())
# plt.yticks(())
#
# # plt.show()
plt.show()
# plt.bar(X_bar[p], coef[1][p], color='g')
#
# plt.show()
# plt.bar(X_bar[p], coef[2][p], color='b')
#
# plt.show()
