from src.networksecurity import logger
from src.networksecurity.utils.common import load_object
from src.networksecurity import constants as const

class PredictionPipeline:
    def __init__(self):
        logger.info("Initialized Prediction Pipeline")
        self.preprocessor = load_object(const.PREPROCESSOR_MODEL)
        logger.info(f"model path: {const.FINAL_MODEL}")
        self.model = load_object(const.FINAL_MODEL)
    
    def predict(self, prediction_df):
        try:
            logger.info("Inside predict method of Prediction Pipeline")
            logger.info(f"preprocessoer model:{type(self.preprocessor)}")
            logger.info(f"prediction model:{type(self.model)}")
            processed_data = self.preprocessor.transform(prediction_df)
            pred = self.model.predict(processed_data)
            return pred
            
        except Exception as e:
            logger.error(f"Error occured inside predict method of Prediction Pipeline: {e}")
            raise e