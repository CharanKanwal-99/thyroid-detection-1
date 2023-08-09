import dill
from sklearn.metrics import r2_score,accuracy_score

def save_object(object,file_path):
    with open(file_path) as file:
        dill.dump(object,file)

def object_loader(file_path):
    with open(file_path) as file:
        object = dill.load(file)
    return object

def find_redundant(df):
    percent_missing = (df.isna().sum()/len(df))*100
    to_drop = []
    for key,val in percent_missing.items():
        if val > 20:
            to_drop.append(key)
    return to_drop

def evaluate_model(X_train, X_test, Y_train,Y_test,models):
    model.fit(X_train,Y_train)
    pred = model.predict(X_test)
    r2 = r2_score(pred,Y_test)
    accuracy = accuracy_score(pred,Y_test)
