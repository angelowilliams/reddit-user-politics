import pandas
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def createModels():
    data = pandas.read_excel('data.xlsx')

    xLabels = list(data.iloc[:, 0])
    yLabels = list(data.iloc[:, 1])
    features = data.iloc[:, 2:]

    xTrain, xTest, yTrain, yTest, featuresTrain, featuresTest = \
        train_test_split(xLabels, yLabels, features, test_size=0.1)

    xModel = RandomForestRegressor(n_estimators=250)
    yModel = RandomForestRegressor(n_estimators=250)

    for model, labelTrain, labelTest, name in [[xModel, xTrain, xTest, 'x'],
                                        [yModel, yTrain, yTest, 'y']]:
        model.fit(featuresTrain, labelTrain)
        pred = xModel.predict(featuresTest)
        print(labelTest)
        print(pred)
        print('')
        print(mean_squared_error(labelTest, pred))

    return xModel, yModel
