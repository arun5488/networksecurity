from src.networksecurity import logger
import yaml
import os
from pathlib import Path
from box import ConfigBox
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import numpy as np
import pickle


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

    
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        logger.info("Inside save_numpy_array_data method")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        logger.error(f"error occured in save_numpy_array_data: {e}")
        raise e
    
def save_object(file_path: str, obj: object) -> None:
    try:
        logger.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logger.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        logger.error(f"error occured in save_numpy_array_data: {e}")
        raise e
    
def load_object(file_path: str ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            logger.info(file_obj)
            obj =  pickle.load(file_obj)
            if obj is None:
                raise ValueError(f"Loaded object from {file_path} is None")
            logger.info(f"Successfully loaded object from {file_path}")
            return obj

    except Exception as e:
        logger.error(f"error occured in save_numpy_array_data: {e}")
        raise e
    
def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        logger.error(f"error occured in save_numpy_array_data: {e}")
        raise e
    
