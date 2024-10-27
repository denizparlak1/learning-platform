import io
import boto3
from fastapi import Depends

from service.s3.config.s3_config import S3Config, get_s3_config


class S3Service:
    def __init__(self, config: S3Config):
        self.client = boto3.client(
            's3',
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key,
            region_name=config.region_name
        )
        self.bucket_name = config.bucket_name

    def upload_file(self, file_path, file_content, content_type=None):
        try:
            response = self.client.upload_fileobj(
                io.BytesIO(file_content),
                self.bucket_name,
                file_path,
                ExtraArgs={"ContentType": content_type}
            )
            return file_path
        except Exception as e:
            raise Exception(f"S3 Error: {e}")

    def delete_file(self, file_path: str):
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=file_path)
            return True
        except Exception as e:
            raise Exception(f"S3 Error: {e}")

    def delete_files_by_prefix(self, prefix: str):
        try:
            objects_to_delete = self.client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            if 'Contents' in objects_to_delete:
                delete_keys = [{'Key': obj['Key']} for obj in objects_to_delete['Contents']]
                delete_keys = [key for key in delete_keys if key['Key'].startswith(prefix) and key['Key'] != prefix]
                if delete_keys:
                    self.client.delete_objects(Bucket=self.bucket_name, Delete={'Objects': delete_keys})
                else:
                    print("No files to delete under the specified prefix.")
            else:
                print("No objects found to delete.")
            return True
        except Exception as e:
            raise Exception(f"S3 Error: {e}")

    def delete_course_by_prefix(self, prefix: str):
        try:
            objects_to_delete = self.client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            if 'Contents' in objects_to_delete:
                delete_keys = [{'Key': obj['Key']} for obj in objects_to_delete['Contents']]
                self.client.delete_objects(Bucket=self.bucket_name, Delete={'Objects': delete_keys})
            else:
                print("No objects found to delete.")
            return True
        except Exception as e:
            raise Exception(f"S3 Error: {e}")


def get_s3_service(config: S3Config = Depends(get_s3_config)) -> S3Service:
    return S3Service(config)
