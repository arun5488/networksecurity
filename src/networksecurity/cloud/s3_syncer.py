import os
from src.networksecurity import logger
class S3Sync:
    def __init__(self):
        logger.info("Initialized S3Sync class")
    
    def sync_local_to_s3(self, local_file_path, aws_bucket_url):
        logger.info("Inside sync_local_to_s3 method")
        logger.info(f"local file path:{local_file_path}")
        logger.info(f"aws bucket URL: {aws_bucket_url}")
        command = f"aws s3 sync {local_file_path} {aws_bucket_url} "
        os.system(command)

    def sync_s3_to_local(self, aws_bucket_url, local_file_path):
        logger.info("Inside sync_s3_to_local folder")
        logger.info(f"aws bucket url:{aws_bucket_url}")
        logger.info(f"local file path:{local_file_path}")
        command = f"aws s3 sync {aws_bucket_url} {local_file_path} "
        os.system(command)