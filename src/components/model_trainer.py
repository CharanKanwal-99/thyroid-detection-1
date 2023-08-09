import os
from dataclasses import dataclass
import numpy as np
from src.utils import evaluate_model, save_object
from imblearn.over_sampling import SMOTE
from src.logger import logging

@dataclass
class ModelTrainerConfig():
    model_file_path = os.path.join("Artifacts","model.pkl")

class ModelTrainer():
    def __init__(self, train_arr,test_arr):
        self.model_trainer_config = ModelTrainerConfig()
        self.train_arr = train_arr
        self.test_arr = test_arr

    def run(self):
        X_train,X_test,Y_train,Y_test = self.oversampling()
        X_train,X_test,Y_train,Y_test = self.feature_selection(X_train,X_test,Y_train,Y_test)
        self.initiate_model_training(X_train,X_test, Y_train,Y_test)

    
    def oversampling(self):
        """
        Method Name: oversampling
        Description: Oversamples the minority class using the SMOTE method to deal with the imbalanced nature of data
        Output: Returns the resampled X and Y dataframes
        """
        X_train, Y_train, X_test, Y_test = self.train_arr[:-1], self.train_arr[-1], self.test_arr[:-1], self.test_arr[-1]
        smote = SMOTE()
        X_resampled, Y_resampled = smote.fit_resample(X_train,Y_train)
        return X_resampled, X_test, Y_resampled, Y_test





    def feature_selection(self,X_train, X_test,Y_train,Y_test):
        """
        Method Name: feature_selection
        Description: Checks for collinearity among predictors and removes highly correlated features
        Output: Returns 4 dataframes i.e X_train, X_test, Y_train,Y_test after removing correlated features
        """
        corr_matrix = X_train.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
        to_drop = [column for column in upper.columns if any(upper[column] > 0.8)]
        X_train.drop(to_drop, axis=1, inplace=True)
        X_test.drop(to_drop, axis=1,inplace=True)
        logging.info("Multicollinearity in data has been dealt with")
        return X_train,X_test,Y_train,Y_test



    def initiate_model_training(self,X_train,X_test,Y_train,Y_test):
        """
        Method Name: initiate_model_training
        Description:Trains the different models on the training data and performs model selection on test data.
        Output: Does not return anything but stores the best performing model in the relevant directory.
        """
        models = {
            'RandomForest': RandomForestClassifier(),
            'LogisticRegressor': LogisticRegression(),
            'XgBoost', XGBClassifier(),
            'LightGBM', LightGBM(),}
        
        evaluate_model(X_train,X_test,Y_train,Y_test,models)
        
        save_object(best_model, self.model_trainer_config.model_file_path)
        logging.info("The best performing model has been saved in the relevant directory")
