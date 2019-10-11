def predict(train_data):
    import numpy as np # linear algebra
    import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
    from sklearn.ensemble import RandomForestClassifier

    test_data = pd.read_csv("test.csv")

    y = train_data["Survived"]

    features = ["Pclass", "Sex", "SibSp", "Parch"]
    X = pd.get_dummies(train_data[features])
    X_test = pd.get_dummies(test_data[features])

    print(X)
    print(X_test)

    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
    model.fit(X, y)
    predictions = model.predict(X_test)

    output = pd.DataFrame({'PassengerId': test_data.PassengerId, 'Survived': predictions})
    output.to_csv('tutorial_prediction.csv', index=False)
    print("Your submission was successfully saved!")