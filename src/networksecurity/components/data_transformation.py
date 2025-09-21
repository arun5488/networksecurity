from src.networksecurity.entity import DataTransformationConfig
import pandas as pd
from src.networksecurity import logger
from src.networksecurity import constants as const
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
import numpy as np
from src.networksecurity.utils.common import save_numpy_array_data, save_object, create_directories

class DataTransformation:
    def __init__(self, config=DataTransformationConfig):
        logger.info("Initializing DataTransformation")
        self.config = config
    
    def get_data_transformer_object(cls)->Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """
        logger.info(
            "Entered get_data_trnasformer_object method of Trnasformation class"
        )
        try:
           imputer:KNNImputer=KNNImputer(**const.DATA_TRANSFORMATION_IMPUTER_PARAMS)
           logger.info(
                f"Initialise KNNImputer with {const.DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
           processor:Pipeline=Pipeline([("imputer",imputer)])
           return processor
        except Exception as e:
            logger.error(f"error occured in get_data_transformer_object: {e}")
            raise e
    
    def initiate_data_transformation(self):
        try:
            logger.info(f"Inside initiate_data_transformation method")
            train_csv = pd.read_csv(self.config.train_data)
            y_train = train_csv[self.config.target_column]
            train_csv.drop(columns=[self.config.target_column], axis=1, inplace= True)
            y_train = y_train.replace(-1,0)

            preprocessor = self.get_data_transformer_object()
            preprocessor_obj = preprocessor.fit(train_csv)
            train_csv_transform = preprocessor_obj.transform(train_csv)
            train_arr = np.c_[train_csv_transform,np.array(y_train)]

            save_numpy_array_data(self.config.train_npy, train_arr)
            logger.info(f"train.npy saved in: {self.config.train_npy}")

            test_csv = pd.read_csv(self.config.test_data)
            y_test = test_csv[self.config.target_column]
            test_csv.drop(columns=[self.config.target_column], axis=1, inplace=True)
            y_test = y_test.replace(-1,0)
            test_csv_transform = preprocessor_obj.transform(test_csv)
            test_arr = np.c_[test_csv_transform,np.array(y_test)]

            save_numpy_array_data(self.config.test_npy, test_arr)
            logger.info(f"test.npy saved in: {self.config.test_npy}")

            #saving the preprocessor 
            create_directories([const.FINAL_MODEL_FOLDER])
            save_object(const.PREPROCESSOR_MODEL, preprocessor_obj)
            logger.info(f"preprocessor model saved in: {const.PREPROCESSOR_MODEL}")

        except Exception as e:
            logger.error(f"error occured inside initiate_data_transformation:{e}")
            raise e