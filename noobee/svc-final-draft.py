from __future__ import division
from sklearn.model_selection import train_test_split, cross_val_score, KFold, cross_val_predict
from sklearn import svm
import numpy as np

from sklearn.metrics import roc_curve, auc

from sklearn.preprocessing import label_binarize, normalize, scale, StandardScaler, LabelBinarizer, Normalizer
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.model_selection import StratifiedKFold, learning_curve
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix, classification_report
# from sklearn.multiclass import OneVsRestClassifier
import itertools
from sklearn.decomposition import PCA as sklearnPCA
h = .02

def make_meshgrid(x, y, h=.02):
    """Create a mesh of points to plot in

    Parameters
    ----------
    x: data to base x-axis meshgrid on
    y: data to base y-axis meshgrid on
    h: stepsize for meshgrid, optional

    Returns
    -------
    xx, yy : ndarray
    """
    x_min, x_max = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1, y.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    return xx, yy

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

def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    """
    Generate a simple plot of the test and training learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:
          - None, to use the default 3-fold cross-validation,
          - integer, to specify the number of folds.
          - An object to be used as a cross-validation generator.
          - An iterable yielding train/test splits.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt

random_state = np.random.RandomState(0)

clf = OneVsRestClassifier(make_pipeline(StandardScaler(), svm.SVC(kernel='linear', probability=True, random_state=random_state)))
# clf = svm.SVC(kernel='linear', probability=True, random_state=random_state)

X = np.genfromtxt('diffuse-trees-75-with-1wk.csv', delimiter=',')
# X = scale(X)
# X = normalize(X, axis=1)
#
# ash_label = np.full((300,), 0)
# oak_label = np.full((300,), 1)
# maple_label = np.full((300,),2)
#
ash_label = np.full((600,), 0)
oak_label = np.full((600,), 1)
maple_label = np.full((600,),2)



# grit_220 = np.full((100,), 3)
# grit_150 = np.full((100,), 2)
# grit_100 = np.full((100,), 1)
# grit_60 = np.full((100,), 0)
y = np.concatenate((ash_label, oak_label, maple_label))
# y = np.concatenate((grit_60, grit_100, grit_150, grit_220))
# y = label_binarize(y, classes=[0,1,2])
# cv = StratifiedKFold(n_splits=6)
cv = StratifiedKFold(2, shuffle=True)
# y = LabelBinarizer().fit_transform(y)

# Plot the confusion matrix to determine the fp tp etc
# class_names = ['ash', 'oak', 'maple']
class_names = ['60 Grit', '100 Grit', '150 Grit', '220 Grit']
prediction = cross_val_predict(clf, X, y, cv=cv)
print "CLASKLHF", classification_report(y, prediction)
cnf_matrix = confusion_matrix(y, prediction)
plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                      title='Normalized confusion matrix')

plt.show()

# Plot the learning curve to show training set bias
plot_learning_curve(clf, 'Learning Curve', X, y, (0, 1.01), cv=cv, n_jobs=4)
plt.show()
#
i = 1
tprs = dict()
aucs = dict()

tprs[0] = []
tprs[1] = []
tprs[2] = []
tprs[3] = []

aucs[0] = []
aucs[1] = []
aucs[2] = []
aucs[3] = []

mean_fpr = dict()
mean_fpr[0] = np.linspace(0, 1, 100)
mean_fpr[1] = np.linspace(0, 1, 100)
mean_fpr[2] = np.linspace(0, 1, 100)
mean_fpr[3] = np.linspace(0, 1, 100)


#
#
#
# for train, test in cv.split(X, y):
#     # print X[train].shape
#     # print y[train].shape
#     # print y[test].shape
#
#     y_test = label_binarize(y[test], classes=[0,1,2])
#
#     # X = X.reshape(-1,1)
#
#     fit = clf.fit(X[train], y[train])
#
#     y_pred = fit.predict(X[test])
#     # print fit
#     # print "FIT", clf.estimator.named_steps['svc'].best_params_
#     print classification_report(y[test], y_pred)
# # binarize the labels for roc_curve
# # y = label_binarize(y, classes=[0,1,2])
#
#     y_score = clf.fit(X[train], y[train]).decision_function(X[test])
#
#
#
#
#     # coef = clf.estimator.named_steps['svc']
#     # # print "coef", coef
#     # print coef
#     #
#     # feature_labels = ['S1_b mean', 'S1_b std', 'S1_g mean', 'S1_g std', 'S1_r mean', 'S1_r std', 'S2_b mean', 'S2_b std', 'S2_g mean', 'S2_g std', 'S2_r mean', 'S2_r std', 'H_b diss','H_b contrast', 'H_b corr', 'H_b energy', 'H_g diss','H_g contrast', 'H_g corr', 'H_g energy', 'H_r diss','H_r contrast', 'H_r corr', 'H_r energy', 'V_b diss','V_b contrast', 'V_b corr', 'V_b energy', 'V_g diss','V_g contrast', 'V_g corr', 'V_g energy', 'V_r diss','V_r contrast', 'V_r corr', 'V_r energy',
#     # 'P_b diss','P_b contrast', 'P_b corr', 'P_b energy', 'P_g diss','P_g contrast', 'P_g corr', 'P_g energy', 'P_r diss','P_r contrast', 'P_r corr', 'P_r energy', 'M_b diss','M_b contrast', 'M_b corr', 'M_b energy', 'M_g diss','M_g contrast', 'M_g corr', 'M_g energy', 'M_r diss','M_r contrast', 'M_r corr', 'M_r energy']
#     # X_bar = np.arange(0,coef.shape[1],1)
#     # p = coef[0].argsort()
#     #
#     # plt.bar(X_bar, coef[0], color='r')
#     # plt.xticks(X_bar, feature_labels, rotation=90)
#     # plt.show()
#
#
#     # Reduct the dimensionality of the data for plotting
#
#
#
#
#
#
#
#
#
#
#
#
#
#     pca = sklearnPCA(n_components=2)
#     X_2d_train = pca.fit_transform(X[train])
#     print "X_2d_train"
#     X_2d_train = StandardScaler().fit_transform(X_2d_train)
#
#     X_2d_test = pca.fit_transform(X[test])
#     X_2d_test = StandardScaler().fit_transform(X_2d_test)
#
#     X0, X1 = X_2d_train[:, 0], X_2d_train[:, 1]
#
#
#
#
#     # Create meshgrid to predict values across entire range
#     xx, yy = make_meshgrid(X0, X1)
#     # Z = Z.reshape(xx.shape)
#     Z = clf.fit(X_2d_train, y[train]).predict_proba(X_2d_train)
#     # plt.scatter(clf.support_vectors_[:,0], clf.support_vectors_[:,1])
#     Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
#     Z = Z.reshape(xx.shape)
#     print "Z", Z
#
#     print "y test", Z
#     plt.contourf(xx,yy,Z, alpha=0.4)
#
#     plt.scatter(X0, X1, color=['r', 'g', 'b', 'm'], label=['American Ash', 'Red Oak', 'Sugar Maple'])
#     plt.legend()
#     plt.show()
#
#     # print "ERICKSEN", clf.estimator.named_steps['svc'
#
#
#     # Compute ROC curve and area the curve
#     fpr = dict()
#     tpr = dict()
#     roc_auc = dict()
#
#     # Iterate through each class to predict the fpr and tpr for each class
#     for j in [0,1,2]:
#
#
#         fpr[j], tpr[j], _ = roc_curve(y_test[:, j], y_score[:, j])
#         roc_auc[j] = auc(fpr[j], tpr[j])
#         aucs[j].append(roc_auc[j])
#
#         tprs[j].append(np.interp(mean_fpr[j], fpr[j], tpr[j]))
#
#
#         # print "roc_auc", roc_auc[j]
#         # aucs[j].append(roc_auc[j])
#
#         # plt.plot(fpr[j], tpr[j], lw=1, alpha=0.3,
#         #          label='ROC fold %d, Class %d (AUC = %0.2f)' % (i, j, roc_auc[j]))
#
#     i += 1
#
# # plt.show()
#
# # TODO make this handle more validation folds andbe a function
# # fpr_0_avg = np.mean((fprs[0][0] + fprs[0][1]) / 2)
# print "NICHOLAS", aucs
# fpr_0_avg = mean_fpr[0]
# tpr_0_avg = np.mean(tprs[0], axis=0)
# mean_0_auc = auc(fpr_0_avg, tpr_0_avg)
# std_0_auc = np.std(aucs[0])
# std_tpr_0 = np.std(tprs[0], axis=0)
# tprs_upper_0 = np.minimum(tpr_0_avg  + std_tpr_0, 1)
# tprs_lower_0 = np.maximum(tpr_0_avg  - std_tpr_0, 0)
# plt.fill_between(fpr_0_avg, tprs_lower_0, tprs_upper_0, color='g', alpha=.2)
# print "jsdkfhkjsd", aucs
# print tprs[0]
# plt.plot(fpr_0_avg, tpr_0_avg ,color='g', lw=4, label='Class 0 Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_0_auc, std_0_auc))
#
# fpr_1_avg = mean_fpr[1]
# tpr_1_avg = (tprs[1][0] + tprs[1][1]) /2
# mean_1_auc = auc(fpr_1_avg, tpr_1_avg)
# std_1_auc = np.std(aucs[1])
#
# std_tpr_1 = np.std(tprs[1], axis=0)
# tprs_upper_1 = np.minimum(tpr_1_avg  + std_tpr_1, 1)
# tprs_lower_1 = np.maximum(tpr_1_avg  - std_tpr_1, 0)
# plt.fill_between(fpr_1_avg, tprs_lower_1, tprs_upper_1, color='r', alpha=.2)
# print "jsdkfhkjsd", std_tpr_0
# print tprs[0]
# plt.plot(fpr_1_avg, tpr_1_avg , lw=4, color='r', label='Class 1 Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_1_auc, std_1_auc))
#
# fpr_2_avg = mean_fpr[2]
# tpr_2_avg = (tprs[2][0] + tprs[2][1]) /2
# mean_2_auc = auc(fpr_2_avg, tpr_2_avg)
# std_2_auc = np.std(aucs[2])
# std_tpr_2 = np.std(tprs[2], axis=0)
# tprs_upper_2 = np.minimum(tpr_2_avg  + std_tpr_2, 1)
# tprs_lower_2 = np.maximum(tpr_2_avg  - std_tpr_2, 0)
# plt.fill_between(fpr_2_avg, tprs_lower_2, tprs_upper_2, color='b', alpha=.2)
# print "jsdkfhkjsd", std_tpr_0
# print tprs[0]
# plt.plot(fpr_2_avg, tpr_2_avg , lw=4, color='b', label='Class 2 Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_2_auc, std_2_auc))
#
# # fpr_3_avg = mean_fpr[3]
# # tpr_3_avg = (tprs[3][0] + tprs[3][1]) /2
# # mean_3_auc = auc(fpr_3_avg, tpr_3_avg)
# # std_3_auc = np.std(aucs[3])
# # std_tpr_3 = np.std(tprs[3], axis=0)
# # tprs_upper_3 = np.minimum(tpr_3_avg  + std_tpr_3, 1)
# # tprs_lower_3 = np.maximum(tpr_3_avg  - std_tpr_3, 0)
# # plt.fill_between(fpr_3_avg, tprs_lower_3, tprs_upper_3, color='y', alpha=.2)
# # print "jsdkfhkjsd", std_tpr_0
# # print tprs[0]
# # plt.plot(fpr_3_avg, tpr_3_avg , lw=4, color='b', label='Class 2 Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_3_auc, std_3_auc))
#
# plt.legend(loc='best')
# plt.title('Receiver Operating characteristic (ROC)')
# plt.xlabel('False Postitive Rate')
# plt.ylabel('True Positive Rate')
# plt.show()
