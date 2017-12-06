from __future__ import division
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import svm
import numpy as np

from sklearn.metrics import roc_curve, auc
import itertools
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.metrics import confusion_matrix, classification_report

X = np.genfromtxt('sandpaper-new.csv', delimiter=',')
# print X

# ash_label = np.full((300,), 0)
# oak_label = np.full((300,), 1)
# maple_label = np.full((300,),2)

grit_100 = np.full((300,), 1)
grit_60 = np.full((300,), 0)

# print ash_label
# y = np.concatenate((ash_label, oak_label, maple_label))
y = np.concatenate((grit_60, grit_100))

# binarize the labels for roc_curve
# y = label_binarize(y, classes=[0,1,2])
# y = label_binarize(y, classes=[0,1])
# n_classes = y.shape[1]
# print "n", n_classes
# print y

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
print "X_train shape", X_train.shape
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

clf = svm.SVC(kernel='linear')
y_pred = clf.fit(X_train, y_train).predict(X_test)

# cnf_matrix = confusion_matrix(y_test, y_pred)
# print cnf_matrix
# np.set_printoptions(precision=2)
# print classification_report(y_test, y_pred)

class_names = ['ash', 'oak', 'maple']
# plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
#                       title='Normalized confusion matrix')
coef = clf.coef_
print "coef", coef
print coef.shape

feature_labels = ['S1_b mean', 'S1_b std', 'S1_g mean', 'S1_g std', 'S1_r mean', 'S1_r std', 'S2_b mean', 'S2_b std', 'S2_g mean', 'S2_g std', 'S2_r mean', 'S2_r std', 'H_b diss','H_b contrast', 'H_b corr', 'H_b energy', 'H_g diss','H_g contrast', 'H_g corr', 'H_g energy', 'H_r diss','H_r contrast', 'H_r corr', 'H_r energy', 'V_b diss','V_b contrast', 'V_b corr', 'V_b energy', 'V_g diss','V_g contrast', 'V_g corr', 'V_g energy', 'V_r diss','V_r contrast', 'V_r corr', 'V_r energy',
'P_b diss','P_b contrast', 'P_b corr', 'P_b energy', 'P_g diss','P_g contrast', 'P_g corr', 'P_g energy', 'P_r diss','P_r contrast', 'P_r corr', 'P_r energy', 'M_b diss','M_b contrast', 'M_b corr', 'M_b energy', 'M_g diss','M_g contrast', 'M_g corr', 'M_g energy', 'M_r diss','M_r contrast', 'M_r corr', 'M_r energy']
X_bar = np.arange(0,60,1)
p = coef[0].argsort()

plt.bar(X_bar, coef[0], color='r')
plt.xticks(X_bar, feature_labels, rotation=17)
plt.show()
# plt.bar(X_bar[p], coef[1][p], color='g')
#
# plt.show()
# plt.bar(X_bar[p], coef[2][p], color='b')
#
# plt.show()
