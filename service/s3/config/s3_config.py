from config.enviroment.env_config import settings


class S3Config:
    def __init__(self):
        self.aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        self.region_name = settings.AWS_REGION
        self.bucket_name = settings.AWS_S3_BUCKET_NAME


def get_s3_config() -> S3Config:
    return S3Config()