from dataclasses import dataclass
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import os
import numpy as np
import pandas as pd
from src.utils import save_object
from src.utils import find_redundant
from src.logger import logging


@dataclass
class DataTransformationConfig():
    transformer_object_path = os.path.join("Artifacts/preprocessor.pkl")


class DataTransformation():
    def __init__(self,train_path,test_path):
        self.transformer_config = DataTransformationConfig()
        self.train_path = train_path
        self.test_path = test_path
    
    def run(self):
        """
        Method Name: run
        Description: performs all the operations of the Data Transformation class
        Output: Returns two dataframes i.e the train and test array after performing outlier removal, imputation, scaling and encoding
        """
        df_train, df_test = self.outlier_treatment()
        df_train,df_test = self.incorrect_to_null(df_train,df_test)
        df_train, df_test = self.redundant_columns(df_train, df_test)
        train_arr,test_arr = self.initiate_data_transformation(df_train,df_test)
        return train_arr,test_arr



    def outlier_treatment(self):
        """
        Method Name: outlier_treatment
        Description: Removes the outliers in the training data using IQR Formula
        Output: Returns the train and test dataframes obtained after removing outliers
        """
        df_train = pd.read_csv(self.train_path)
        df_test = pd.read_csv(self.test_path)
        q1 = df_train.quantile(0.25)
        q3 = df_train.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        df_train = df_train.mask((df_train < lower_bound) | (df_train > upper_bound))
        logging.info("Outliers have been removed from data using IQR Formula")
        return df_train, df_test
    

    def incorrect_to_null(self, df_train,df_test):
        """
        Method: incorrect_to_null
        Description: Converts the values recorded as "?" to null values
        Output: Returns train and test dataframe obtained after the substitution operation
        """
        df_train.replace("?", np.nan, inplace=True)
        df_test.replace("?", np.nan, inplace=True)
        return df_train,df_test

    
    def redundant_columns(self,df_train, df_test):
        """
        Method: redundant_columns
        Description: Drops the columns in data with more than 20% percent missing values
        Output: Returns the train and test dataframes after removal of necessary columns
        """
        cols = find_redundant(df_train)
        df_train.drop(cols,axis=1,inplace=True)
        df_test.drop(cols,axis=1,inplace=True)
        logging.info("Redundant columns have been removed")
        return df_train, df_test
    
    
    def get_transformer_object(self,df_train):
        """
        Method Name: get_transformer_object
        Description: Creates the transformer/preprocessor object which will be used for imputation, scaling and feature encoding
        Output: Returns the preprocessor/transformer object created
        """
        target_column = "Class"
        input_feature_df = df_train.drop(target_column, axis=1)
 
        num_col = input_feature_df.select_dtypes(exclude='object').columns
        cat_col = input_feature_df.select_dtypes(include='object').columns

        skew_col = []
        num_normal = [x for x in num_col if x not in skew_col]
        
        # Pipeline for numeric columns with normal distribution
        num_normal_pipeline = Pipeline(
            steps= [('imputer', SimpleImputer(strategy='mean')), ('scaler', StandardScaler())]
        )
        
        # Pipeline for numeric columns with skewed distribution
        num_skew_pipeline = Pipeline(
            steps= [('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())]
        )
        
        # Pipeline for categorical columns 
        cat_pipeline = Pipeline(
            steps= [('imputer', SimpleImputer(strategy='most_frequent')), ('encoder', OneHotEncoder())]
        )


        preprocessor_obj = ColumnTransformer([('num_normal_pipeline',num_normal_pipeline, num_normal), ('num_skew_pipeline', num_skew_pipeline, skew_col) ('cat_pipeline',cat_pipeline, cat_col)])

        
        logging.info("Preprocessor Object has been created")
        return preprocessor_obj
    

    
    
    def initiate_data_transformation(self,df_train,df_test):
        """
        Method: initiate_data_transformation
        Description: Performs the process of data transformation using the transformer object created
        Output: Returns the train and test array after the completed preprocessing

        """
        preprocessor_obj = self.get_transformer_object(df_train)
        target_column = "Class"
        input_feature_df = df_train.drop(target_column, axis=1)
        input_target_df = df_train[target_column]
        test_feature_df = df_test.drop(target_column, axis=1)
        test_target_df = df_train[target_column]
        input_feature_scaled = preprocessor_obj.fit_transform(input_feature_df)
        test_feature_scaled = preprocessor_obj.transform(test_feature_df)
        save_object(preprocessor_obj, self.transformer_config.transformer_object_path)
        logging.info("Preprocessor object has been stored in relevant directory")
        train_arr = np.c(input_feature_scaled, np.array(input_target_df))
        test_arr = np.c(test_feature_scaled, np.array(test_target_df))
        logging.info("Train and Test dataframes have been created")

        return train_arr, test_arr
    
