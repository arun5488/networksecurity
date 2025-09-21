from src.networksecurity.components.data_transformation import DataTransformation
from src.networksecurity.config.configuration import ConfigurationManager
from src.networksecurity import logger

class DataTransformationPipeline():
    def __init__(self):
        logger.info("Initializing Data Transformation Pipeline")
        self.config = ConfigurationManager().get_data_transformation_config()
    
    def initiate_data_transformation_pipeline(self):
        try:
            logger.info("Inside initiate_data_transformartion")
            DataTransformation(self.config).initiate_data_transformation()
            
        except Exception as e:
            logger.error(f"error in initiate_data_transformation_pipeline:{e}")
            raise e