from src.networksecurity.components.data_validation import DataValidation
from src.networksecurity.config.configuration import ConfigurationManager
from src.networksecurity import logger

class DataValidationPipeline:
    def __init__(self):
        logger.info("Initializing DataValidationPipeline")
        self.config = ConfigurationManager().get_data_validation_config()
    
    def initiate_data_validation_pipeline(self):
        try:
            logger.info("Inside initiate_data_validation_pipeline")
            data_validataion = DataValidation(self.config)
            data_validataion.initiate_data_validation()
        except Exception as e:
            logger.error(f"error occured in initiate_data_validation_pipeline: {e}")
            raise e
        