from src.networksecurity.components.model_trainer import ModelTrainer
from src.networksecurity import logger
from src.networksecurity.config.configuration import ConfigurationManager

class ModelTrainerPipeline:
    def __init__(self):
        logger.info("Initialized ModelTrainerPipeline")
        self.config = ConfigurationManager().get_model_trainer_config()
    
    def initiate_model_trainer_pipeline(self):
        try:
            logger.info("Inside initiate_model_trainer_pipeline config")
            model_trainer = ModelTrainer(self.config)
            logger.info("Initaiting model training")
            model_trainer.initiate_model_trainer()
            logger.info("Model training completed")

        except Exception as e:
            logger.error(f"Error occured inside initiate_model_trainer_pipeline:{e}")
            raise e
        
