from __future__ import division
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import svm
import numpy as np

from sklearn.metrics import roc_curve, auc

from sklearn.preprocessing import label_binarize, normalize, scale
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp
import matplotlib.pyplot as plt
from itertools import cycle

X = np.genfromtxt('specular-trees.csv', delimiter=',')
X = scale(X)
# X = normalize(X, axis=0)
# print X

ash_label = np.full((300,), 0)
oak_label = np.full((300,), 1)
maple_label = np.full((300,),2)

# grit_220 = np.full((100,), 3)
# grit_150 = np.full((100,), 2)
# grit_100 = np.full((100,), 1)
# grit_60 = np.full((100,), 0)


# print ash_label
y = np.concatenate((ash_label, oak_label, maple_label))
# y = np.concatenate((grit_60, grit_100, grit_150, grit_220))

# binarize the labels for roc_curve
# y = label_binarize(y, classes=[0,1,2])
y = label_binarize(y, classes=[0,1,2])
n_classes = y.shape[1]
print "n", n_classes
# print y

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)


#############################################
# roc specific
classifier = OneVsRestClassifier(svm.SVC(kernel='linear', C=1))
y_score = classifier.fit(X_train, y_train).decision_function(X_test)

# Compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Compute micro-average ROC curve and ROC area
fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

# plt.figure()
lw = 2
# plt.plot(fpr[2], tpr[2], color='darkorange',
#          lw=lw, label='ROC curve (area = %0.2f)' % roc_auc[2])
# plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('Receiver operating characteristic')
# plt.legend(loc="lower right")
# plt.show()


# Compute macro-average ROC curve and ROC area

# First aggregate all false positive rates
all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

# Then interpolate all ROC curves at this points
mean_tpr = np.zeros_like(all_fpr)
for i in range(n_classes):
    mean_tpr += interp(all_fpr, fpr[i], tpr[i])

# Finally average it and compute AUC
mean_tpr /= n_classes

fpr["macro"] = all_fpr
tpr["macro"] = mean_tpr
roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

# Plot all ROC curves
plt.figure()
plt.plot(fpr["micro"], tpr["micro"],
         label='micro-average ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["micro"]),
         color='deeppink', linestyle=':', linewidth=4)

plt.plot(fpr["macro"], tpr["macro"],
         label='macro-average ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["macro"]),
         color='navy', linestyle=':', linewidth=4)

colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
for i, color in zip(range(n_classes), colors):
    plt.plot(fpr[i], tpr[i], color=color, lw=lw,
             label='ROC curve of class {0} (area = {1:0.2f})'
             ''.format(i, roc_auc[i]))

plt.plot([0, 1], [0, 1], 'k--', lw=lw)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristics')
plt.legend(loc="lower right")
plt.show()


#############################################
print "split"
# clf = svm.SVC(kernel='linear', C=1)
#
# fit = clf.fit(X_train, y_train)
#
# #simple score
# score = fit.score(X_test, y_test)
# print score

# corss validated scores
scores = cross_val_score(classifier, X, y, cv=10)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
