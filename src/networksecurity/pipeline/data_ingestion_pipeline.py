from src.networksecurity.components.data_ingestion import DataIngestion
from src.networksecurity.config.configuration import ConfigurationManager
from src.networksecurity import logger
from src.networksecurity import constants as const

class DataIngestionPipeline:
    def __init__(self):
        logger.info("Starting Data Ingestion Pipeline")
        self.config = ConfigurationManager().get_data_ingestion_config()
    
    def initiate_data_ingestion_pipeline(self):
        try:
            logger.info("Inside initiate_data_ingestion_pipeline method")
            data_ingestion = DataIngestion(config = self.config)
            data_ingestion.initiate_data_ingestion()
            logger.info("Data Ingestion Pipeline completed successfully")
        except Exception as e:
            logger.error(f"Error occured in initiate_data_ingestion_pipeline: {e}")
            raise e