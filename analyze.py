import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder


import xgboost
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression


from sklearn.metrics import explained_variance_score
import matplotlib.pyplot as plt
from sklearn.cross_validation import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import learning_curve


def plot_confusion_matrix(true_value, predict_value, name):
    cm = confusion_matrix(true_value, predict_value)
    plt.matshow(cm, cmap=plt.cm.Greens)
    plt.colorbar()
    plt.ylabel('True value label')
    plt.xlabel('Predicted value label')
    plt.title(name)
    for x in range(len(cm)):
        for y in range(len(cm)):
            plt.annotate(cm[x, y], xy=(x, y), horizontalalignment='center',
                         verticalalignment='center')
    plt.show()


def plot_learning_curve(name, ml_tool, X, y, cv):
    train_sizes, train_scores, test_scores = learning_curve(
            ml_tool, X=X, y=y, cv=cv, n_jobs=1, train_sizes=np.linspace(.1,
                                                                        1.0, 8))
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.figure()
    plt.title("Learning Curve of "+name)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    plt.gca().invert_yaxis()

    plt.grid()
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                        train_scores_mean + train_scores_std, alpha=0.1,
                        color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                        test_scores_mean + test_scores_std, alpha=0.1,
                     color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
                 label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
                label="Cross-validation score")

    plt.legend(loc="best")
    plt.show()

if __name__ == '__main__':
    flights = pd.read_csv("august_7_result.csv")
    flights = flights.loc[flights["airline"] == "Air Canada"]
    print("different prices: \n", flights.groupby(['price']).size())

    print("\n10 random data : \n", flights.loc[np.random.permutation(flights.index)[:10]])
    print("\nNumber of Features/Columns : ", len(flights.columns)-1)
    print("\nNumber of Rows : ", len(flights))
    flights = flights.astype({"price": int})

    train, test = train_test_split(flights, test_size=0.3, random_state=10, shuffle=True)

    xTrain = train.drop('price', axis=1)
    yTrain = train['price']
    xTest = test.drop('price', axis=1)
    yTest = test['price']

    le1 = LabelEncoder()
    le2 = LabelEncoder()

    for col in xTrain.columns:
        xTrain[col] = le1.fit_transform(xTrain[col])
        xTest[col] = le2.fit_transform(xTest[col])

    sc = StandardScaler()
    xTrain = sc.fit_transform(xTrain)
    xTest = sc.transform(xTest)

    assert len(xTrain) == len(yTrain)
    assert len(xTest) == len(yTest)

    xgb = xgboost.XGBRegressor(n_estimators=100, learning_rate=0.05, gamma=0, subsample=0.8,
                                    colsample_bytree=1, max_depth=14)
    xgb.fit(xTrain, yTrain)
    trains1 = xgb.predict(xTrain)
    predictions1 = xgb.predict(xTest)

    randomForest = RandomForestRegressor(n_estimators=100, max_depth=17, max_features="auto",
                                         bootstrap=True, warm_start=True)
    randomForest.fit(xTrain, yTrain)
    trains2 = randomForest.predict(xTrain)
    predictions2 = randomForest.predict(xTest)

    # lr = LogisticRegression(random_state=0, solver="sag", max_iter=500)
    # lr.fit(xTrain, yTrain)
    # trains = lr.predict(xTrain)
    # predictions = lr.predict(xTest)

    bgr = BaggingRegressor(n_estimators=100, max_features=11, bootstrap=True, warm_start=False, oob_score=False)
    bgr.fit(xTrain, yTrain)
    trains3 = bgr.predict(xTrain)
    predictions3 = bgr.predict(xTest)

    final_train = pd.DataFrame()
    final_test = pd.DataFrame()
    final_train['feature1'] = trains1
    final_test['feature1'] = predictions1
    final_train['feature2'] = trains2
    final_test['feature2'] = predictions2
    final_train['feature3'] = trains3
    final_test['feature3'] = predictions3

    lr = LinearRegression()
    lr.fit(final_train, yTrain)
    trains = lr.predict(final_train)
    predictions = lr.predict(final_test)

    print("\ntrain score: ", explained_variance_score(trains, yTrain))
    print("\ntest score: ", explained_variance_score(predictions, yTest))
    trains_array = np.array(trains).tolist()
    yTrain_array = np.array(yTrain).tolist()
    predictions_array = np.array(predictions).tolist()
    yTest_array = np.array(yTest).tolist()
    res = 0
    res1 = 0
    for j in range(len(trains_array)):
        res = res + abs(trains_array[j] - yTrain_array[j])/trains_array[j]
    for j in range(len(predictions_array)):
        res1 = res1 + abs(predictions_array[j] - yTest_array[j])/predictions_array[j]

    print("\nprice error rate of train set: ", res/len(trains_array))
    print("\nprice error rate of test set: ", res1/len(predictions_array))

    X = xTrain
    y = yTrain
    xg = xgboost.XGBRegressor(n_estimators=100, learning_rate=0.06, gamma=0, subsample=0.8,
                                colsample_bytree=1, max_depth=13)

    score = cross_val_score(xg, X, y, cv=10)
    print("\n10-fold cross validation: ", np.mean(score))

    xgg = xgboost.XGBRegressor(n_estimators=100, learning_rate=0.06, gamma=0, subsample=0.8,
                        colsample_bytree=1, max_depth=13)
    cv = KFold(X.shape[0], n_folds=10, random_state=10)
    plot_learning_curve("Learning Curve", xgg, X, y, cv)




