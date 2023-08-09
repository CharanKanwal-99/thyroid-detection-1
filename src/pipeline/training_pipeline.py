from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

class TrainingPipeline():
    def __init__(self):
        pass

    def train(self):
        ingestion_obj = DataIngestion()
        train_path, test_path = ingestion_obj.initiate_data_ingestion()
        transformation_obj = DataTransformation(train_path,test_path)
        train_arr,test_arr = transformation_obj.run()
        trainer_obj = ModelTrainer(train_arr,test_arr)
        trainer_obj.run()
