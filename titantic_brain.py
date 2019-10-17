def predict(train_data, survived_frame):
    import numpy as np # linear algebra
    import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
    from sklearn.neural_network import MLPClassifier

    test_data = pd.read_csv("test.csv", names=['PassengerId','Pclass','Name','Sex','Age','SibSp','Parch','Ticket','Fare','Cabin','Embarked'])
    test_data = test_data.drop(test_data.index[0])
    test_data = test_data.drop('Name', axis = 1)
    test_data = test_data.drop('Ticket', axis = 1)

    y = survived_frame

    print(train_data.iloc[2])

    features = ["Pclass", "Sex", "SibSp"]
    X = pd.get_dummies(train_data[features])
    X_test = pd.get_dummies(test_data[features])

    model = MLPClassifier()
    model.get_params(deep=True)
    model.fit(X, y)
    predictions = model.predict(X_test)

    output = pd.DataFrame({'PassengerId': test_data.PassengerId, 'Survived': predictions})
    output.to_csv('tutorial_prediction.csv', index=False)
    print("Your submission was successfully saved!")