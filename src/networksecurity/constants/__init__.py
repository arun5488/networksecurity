import numpy as np
## YAML file paths
CONFIG_YAML="config/config.yaml"
PARAMS_YAML="params.yaml"
SCHEMA_YAML="schema.yaml"

## train test split ratio
TRAIN_TEST_SPLIT_RATIO=0.2

## data transformation
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}
FINAL_MODEL_FOLDER = "data"
PREPROCESSOR_MODEL = "data/preprocessor.pkl"
FINAL_MODEL = "data/model.pkl"

## model_trainer
MODEL_TRAINER_EXPECTED_SCORE=0.6
MODEL_TRAINER_FITTING_THRESHOLD= 0.05
ENV_DAGSHUB='Y'