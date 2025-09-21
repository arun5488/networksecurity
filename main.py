from src.networksecurity.pipeline.training_pipeline import TrainingPipeline
from src.networksecurity import logger

if __name__ == "__main__":
    try:
        logger.info("Triggering Training Pipeline from main.py")
        TrainingPipeline().initiate_training_pipeline()
        logger.info("Training Pipeline completed successfully")
    except Exception as e:
        logger.error(f"Error occured in main.py: {e}")
        raise e