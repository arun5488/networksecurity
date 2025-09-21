from src.networksecurity.entity import DataValidationConfig
import pandas as pd
from src.networksecurity import logger
from sklearn.model_selection import train_test_split

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        try:
            logger.info("Initiatlized Data Validation")
            self.config = config
        except Exception as e:
            logger.error(f"Error occured in DataValidation: {e}")
            raise e
    
    def initiate_data_validation(self):
        try:
            logger.info(" Inside initiate_data_validation method")
            raw_data = pd.read_csv(self.config.raw_data)
            raw_data_columns = raw_data.columns.tolist()
            schema_columns = self.config.columns
            for column in schema_columns:
                if column not in raw_data_columns:
                    e = ValueError(f"Column {column} is missing from raw data")
                    logger.error(f"Column {column} is missing from raw data")
                    raise e
            logger.info("All columns are present in the raw data")
            # Splitting raw data into train and test sets
            train_data, test_data = train_test_split(raw_data, test_size= self.config.train_test_split_ratio)
            logger.info(f"Raw data length:{len(raw_data.index)}")
            logger.info(f"train data length:{len(train_data.index)}")
            logger.info(f"test data length:{len(test_data.index)}")
            # saving the train and test data
            train_data.to_csv(self.config.train_data, index=False, header = True)
            logger.info(f"train data saved into: {self.config.train_data}")
            test_data.to_csv(self.config.test_data, index=False, header = True)
            logger.info(f"test data saved into: {self.config.test_data}")

        except Exception as e:
            logger.error(f"Error occured in initiate_data_validation: {e}")
            raise e