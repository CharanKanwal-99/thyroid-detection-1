from dataclasses import dataclass
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from logger import logging

@dataclass
class DataIngestionConfig():
    train_data_path = os.path.join("Artifacts","train_data.csv")
    test_data_path = os.path.join("Artifacts","test_data.csv")

class DataIngestion():
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        """
        Method Name: initiate_data_ingestion
        Description: performs data ingestion by ingesting data from source and then splits data into train and test
        Output: returns the path of the train and test data obtained from splitting the ingested data
        """
        df = pd.read_csv("input_file.csv")
        logging.info("Data has been read")
        df_train, df_test = train_test_split(df,test_size=0.2)
        logging.info("Data has been split into train and test")
        df_train.to_csv(self.data_ingestion_config.train_data_path)
        df_test.to_csv(self.data_ingestion_config.test_data_path)
        return (self.data_ingestion_config.train_data_path, self.data_ingestion_config.test_data_path)
    
