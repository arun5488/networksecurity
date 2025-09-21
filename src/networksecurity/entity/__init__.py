from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    raw_data: Path
    target_column: str

@dataclass
class DataValidationConfig:
    root_dir: Path
    raw_data: Path
    train_data: Path
    test_data: Path
    train_test_split_ratio: float
    columns: list

@dataclass
class DataTransformationConfig:
    root_dir: Path
    train_data: Path
    test_data: Path  
    target_column: str
    train_npy: Path
    test_npy: Path
    y_train: Path
    y_test: Path
    knn_inputer: dict