from sklearn import svm
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from matplotlib.colors import ListedColormap
import seaborn as sn


def optimize_hyperparams(X, y, params):
    """
    Hyperparameter optimization of the SVM
    :param X: The feature vectors
    :param y: The labels
    :param params: The grid of all the possible optimal hyperparameters
    :returns: The optimal hyperparameters
    """
    # Optimize hyper-parameters
    model = svm.SVC()
    model_grid_search = GridSearchCV(model, params, cv=10, iid=False, n_jobs=-1)
    model_grid_search.fit(X.values, y.values)
    print("Optimal hyper-parameters: ", model_grid_search.best_params_)
    print("Accuracy :", model_grid_search.best_score_)
    return model_grid_search.best_params_


def classify(X, y, opt_params):
    """
    Classify a feature vector using SVM and print some metrics
    :param X: The feature vectors
    :param y: The labels
    :param opt_params: The optimal hyperparameters
    """
    # Single SVM run with optimized hyperparameters and
    model = svm.SVC(kernel='rbf', gamma=opt_params['gamma'], C=opt_params['C'])
    scores = cross_val_score(model, X, y, cv=10, scoring='accuracy', n_jobs=-1)
    print(scores)
    print(np.mean(scores))
    print(np.std(scores))


def print_confusion_matrix(X, y, opt_params):
    """
    Print the confusion matrix of an SVM classification
    :param X: The feature vectors
    :param y: The labels
    :param opt_params: The optimal hyperparameters
    """
    y_pred, y_test = get_predictions(X, y, opt_params)
    # Printing out false/true positives/negatives
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    print('True negatives: ', tn, 'False positives: ', fp, 'False negatives: ', fn, 'True positives: ', tp)

    # Using seaborn to create a confusion matrix table
    data = {'y_Predicted': y_pred, 'y_Actual': y_test}
    df = pd.DataFrame(data, columns=['y_Actual', 'y_Predicted'])
    conf_matrix = pd.crosstab(df['y_Actual'], df['y_Predicted'], rownames=['Actual'], colnames=['Predicted'])
    sn.heatmap(conf_matrix, cmap=ListedColormap(['#ED7D31', '#009FDA']), annot=True, fmt='g', cbar=False)


def find_misclassified(X, y, opt_params, img_ids):
    """
    Gets the misclassified image ids and writes them to a csv
    :param X: The feature vectors
    :param y: The labels
    :param opt_params: The optimal hyperparameters
    :param img_ids: The image ids that correspond to the feature vector(X)
    """
    y_pred, y_test = get_predictions(X, y, opt_params)
    misclassified = []
    for i in range(len(y_test)):
        if y_pred[i] != y_test.values[i]:
            misclassified.append(str(y_pred[i]) + ',' + str(y_test.values[i]) + ',' + str(img_ids[y_test.index[i]]))
    df = pd.DataFrame(misclassified)
    df.columns = ['Prediction,Actual,ImageName']
    df.to_csv('Misclassified.csv', index=False)


def get_predictions(X, y, opt_params):
    """
    Classification using SVM
    :param X: The feature vectors
    :param y: The labels
    :param opt_params: The optimal hyperparameters
    :returns: The predicted and true labels
    """
    # Run one SVM with 80-20 split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
    model = svm.SVC(kernel='rbf', gamma=opt_params['gamma'], C=opt_params['C'])
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    return y_pred, y_test
