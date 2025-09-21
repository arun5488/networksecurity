from src.networksecurity.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.networksecurity.pipeline.data_validation_pipeline import DataValidationPipeline
from src.networksecurity.pipeline.data_transformation_pipeline import DataTransformationPipeline
from src.networksecurity import logger

class TrainingPipeline:
    def __init__(self):
        logger.info("Starting Training Pipeline")
        pass

    def initiate_training_pipeline(self):
        try:
            logger.info("Inside initiate_training_pipeline method")
            logger.info("Starting Data Ingestion Pipeline from Training Pipeline")
            DataIngestionPipeline().initiate_data_ingestion_pipeline()
            logger.info("Data Ingestion Pipeline completed")
            logger.info("Starting Data validation Pipeline from Training Pipeline")
            DataValidationPipeline().initiate_data_validation_pipeline()
            logger.info("Data Validation stage complete")
            logger.info("Starting Data Transformation Pipeline")
            DataTransformationPipeline().initiate_data_transformation_pipeline()
            logger.info("Data Transformation stage completed")
        except Exception as e:
            logger.error(f"Error occured in initiate_training_pipeline: {e}")
            raise e
    