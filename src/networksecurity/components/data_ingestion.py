from src.networksecurity.config.configuration import ConfigurationManager
from src.networksecurity import logger
from src.networksecurity.utils.common import connect_mongodb
import os
from src.networksecurity import constants as const
from src.networksecurity.entity import DataIngestionConfig
from dotenv import load_dotenv
import pandas as pd
import numpy as np

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        logger.info("Starting Data Ingestion")
        self.config = config
        self.client = connect_mongodb()
        
    
    def export_collection_as_dataframe(self):
        try:
            logger.info("Inside export_collection_as_dataframe method")
            load_dotenv()
            database = self.client[os.getenv("MONGO_DB_NAME")]
            collection = database[os.getenv("MONGO_DB_COLLECTION")]
            df = pd.DataFrame(list(collection.find()))
            if '_id' in df.columns.to_list():
                df.drop(columns=['_id'], inplace=True, axis=1)
            df.replace({"na":np.nan}, inplace = True)
            logger.info("Data exported as dataframe")
            return df
        except Exception as e:
            logger.error(f"error in export_collection_as_dataframe: {e}")
            raise e

    
    def initiate_data_ingestion(self):
        try:
            logger.info("Inside initiate_data_ingestion method")
            raw_data = self.export_collection_as_dataframe()
            logger.info("Saving raw data into csv file")
            raw_data_path = self.config.raw_data
            raw_data.to_csv(raw_data_path, index=False, header=True)
            logger.info("Raw data saved successfully")
        except Exception as e:
            logger.error(f"error in initiate_data_ingestion: {e}")
            raise e
        