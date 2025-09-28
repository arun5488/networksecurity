from src.networksecurity.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.networksecurity.pipeline.data_validation_pipeline import DataValidationPipeline
from src.networksecurity.pipeline.data_transformation_pipeline import DataTransformationPipeline
from src.networksecurity.pipeline.model_trainer_pipeline import ModelTrainerPipeline
from src.networksecurity.cloud.s3_syncer import S3Sync
from src.networksecurity import constants as const
from src.networksecurity.utils.common import read_yaml

from src.networksecurity import logger

class TrainingPipeline:
    def __init__(self):
        logger.info("Starting Training Pipeline")
        self.config = read_yaml(const.CONFIG_YAML)
        self.s3_sync = S3Sync()

    def sync_artifacts_to_s3(self):
        try:
            logger.info("Inside sync_artifacts_to_s3")
            artifacts_folder = f"{self.config.artifacts_root}"
            logger.info(f"artifacts folder:{artifacts_folder}")
            s3_artifacts_folder = f"s3://{const.AWS_BUCKET}/artifact/{artifacts_folder}"
            logger.info(f"s3 artifacts folder:{s3_artifacts_folder}")
            self.s3_sync.sync_local_to_s3(artifacts_folder, aws_bucket_url=s3_artifacts_folder)
        except Exception as e:
            logger.error(f"error occured in sync_artifacts_to_s3:{e}")
            raise e
        
    def sync_data_to_s3(self):
        try:
            logger.info("Inside sync_artifacts_to_s3")
            data_folder = f"{const.FINAL_MODEL_FOLDER}"
            logger.info(f"data folder:{data_folder}")
            s3_artifacts_folder = f"s3://{const.AWS_BUCKET}/data/{data_folder}"
            logger.info(f"s3 artifacts folder:{s3_artifacts_folder}")
            self.s3_sync.sync_local_to_s3(data_folder, aws_bucket_url=s3_artifacts_folder)
        except Exception as e:
            logger.error(f"error occured in sync_artifacts_to_s3:{e}")
            raise e    

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
            logger.info("Starting Model trainer Stage")
            ModelTrainerPipeline().initiate_model_trainer_pipeline()
            logger.info("Model trainer stage completed")

            logger.info("saving artifacts to s3 bucket")
            #syncing artifacts and data to s3
            self.sync_artifacts_to_s3()
            self.sync_data_to_s3()

        except Exception as e:
            logger.error(f"Error occured in initiate_training_pipeline: {e}")
            raise e
    