from src.networksecurity.entity import DataIngestionConfig
from src.networksecurity import logger
from src.networksecurity.utils.common import read_yaml, create_directories
from pathlib import Path
import os
from src.networksecurity import constants as const

class ConfigurationManager:
    def __init__(self):
        logger.info("Initializing Configuration Manager")
        self.config = read_yaml(const.CONFIG_YAML)
        self.schema = read_yaml(const.SCHEMA_YAML)
        self.params = read_yaml(const.PARAMS_YAML)

        create_directories([Path(self.config.artifacts_root)])
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            logger.info("Inside get_data_ingestion_config method")
            data_ingestion_config = self.config.data_ingestion
            logger.info("Creating artifacts directory for data_ingestion")
            create_directories([Path(data_ingestion_config.root_dir)])

            return DataIngestionConfig(
                root_dir=data_ingestion_config.root_dir,
                raw_data=data_ingestion_config.raw_data,
                target_column=data_ingestion_config.target_column
            )

        except Exception as e:
            logger.error(f"Error in get_data_ingestion_config: {e}")
            raise e