from src.networksecurity.entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from src.networksecurity import logger
from src.networksecurity.utils.common import read_yaml, create_directories
from pathlib import Path
import os
from src.networksecurity import constants as const

class ConfigurationManager:
    def __init__(self):
        logger.info("Initializing Configuration Manager")
        self.config = read_yaml(const.CONFIG_YAML)
        self.schema = read_yaml(const.SCHEMA_YAML)
        self.params = read_yaml(const.PARAMS_YAML)

        create_directories([Path(self.config.artifacts_root)])
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            logger.info("Inside get_data_ingestion_config method")
            data_ingestion_config = self.config.data_ingestion
            logger.info("Creating artifacts directory for data_ingestion")
            create_directories([Path(data_ingestion_config.root_dir)])

            return DataIngestionConfig(
                root_dir=data_ingestion_config.root_dir,
                raw_data=data_ingestion_config.raw_data,
                target_column=data_ingestion_config.target_column
            )

        except Exception as e:
            logger.error(f"Error in get_data_ingestion_config: {e}")
            raise e
        
    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            logger.info("Inside get_data_validation_config method")
            data_validation_config = self.config.data_validation
            logger.info("creating directory for data_validation stage")
            create_directories([Path(data_validation_config.root_dir)])

            return DataValidationConfig(
                root_dir = data_validation_config.root_dir,
                raw_data= data_validation_config.raw_data,
                train_data = data_validation_config.train_data,
                test_data = data_validation_config.test_data,
                train_test_split_ratio=const.TRAIN_TEST_SPLIT_RATIO,
                columns=self.schema.columns
            )
        except Exception as e:
            logger.error(f"Error in get_data_validation_config: {e}")
            raise e
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        try:
            logger.info("Inside get_data_transformation_config method")
            data_transformation_config = self.config.data_transformation

            create_directories([data_transformation_config.root_dir])

            return DataTransformationConfig(
                root_dir = data_transformation_config.root_dir,
                train_data = data_transformation_config.train_data,
                test_data = data_transformation_config.test_data,
                target_column = data_transformation_config.target_column,
                train_npy = data_transformation_config.train_npy,
                test_npy = data_transformation_config.test_npy,
                y_train = data_transformation_config.y_train,
                y_test = data_transformation_config.y_test,
                knn_inputer = const.DATA_TRANSFORMATION_IMPUTER_PARAMS
            )

        except Exception as e:
            logger.error(f"Error occured inside get_data_transformation_config: {e}")
            raise e

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        try:
            logger.info("Inside get_model_trainer_config method")
            model_trainer_config = self.config.model_trainer

            create_directories([model_trainer_config.root_dir])

            return ModelTrainerConfig(
                root_dir= model_trainer_config.root_dir,
                train_npy=model_trainer_config.train_npy,
                test_npy=model_trainer_config.test_npy,
                model_name=model_trainer_config.model_name,
                model_expected_score=const.MODEL_TRAINER_EXPECTED_SCORE,
                model_fitting_threshold=const.MODEL_TRAINER_FITTING_THRESHOLD
            )

        except Exception as e:
            logger.error(f"Error occured inside get_model_trainer_config:{e}")
            raise e