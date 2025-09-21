from src.networksecurity import logger
import yaml
import os
from pathlib import Path
from box import ConfigBox
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv


def read_yaml(file_path: Path):
    try:
        logger.info("Inside read_yaml method")
        with open(file_path) as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {file_path} loaded successfully")
            return ConfigBox(config)
    except Exception as e:
        logger.error(f"Error occured in read_yaml: {e}")
        raise e

def create_directories(paths : list):
    try:
        logger.info("Inside create_directories method")
        for path in paths:
            os.makedirs(path, exist_ok = True)
            logger.info(f"Directory created at: {path}")
    except Exception as e:
        logger.error(f"Error occured in create_directories: {e}")
        raise e

def connect_mongodb():
    try:
        logger.info("Inside connect_mongodb method")
        load_dotenv()
        client = MongoClient(os.getenv("MONGO_DB_URL"), server_api = ServerApi('1'))
        logger.info("Connected to MongoDB successfully")
        return client
    except Exception as e:
        logger.error(f"Error occured in connect_mongodb: {e}")
        raise e

