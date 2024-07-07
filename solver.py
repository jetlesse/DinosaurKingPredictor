from sklearn.ensemble import HistGradientBoostingClassifier
import csv
import pickle


def read_model(file):
    """
    read in a saved model file and generate the forest
    :param file: path to a file where a model has been saved
    :return: a forest classifier
    """
    with open(file, "rb") as f:
        return pickle.load(f)


def write_model(clf, file):
    """
    write the current model to a file to be saved for later use
    :param clf: the classifier model object
    :param file: path to the file to save the model in
    :return: None
    """
    with open(file, "wb") as f:
        pickle.dump(clf, f)


def train_model(file):
    """
    train a new model based on the turn data saved in the file
    :param file: path to the file with turn data for the fight
    :return: a forest classifier
    """
    with open(file, "r", newline='') as data_file:
        data = csv.reader(data_file)
        X = []
        y = []
        data.__next__()
        for row in data:
            X.append([int(x) for x in row[:-1]])
            y.append(int(row[-1]))
        clf = HistGradientBoostingClassifier(max_iter=50, min_samples_leaf=5, max_depth=5,
                                             categorical_features=[0, 1, 2, 9, 10]).fit(X, y)
        clf.score(X, y)
        print(clf.score(X, y))
        return clf
