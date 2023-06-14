import boto3
import io

from src.infrastructure.s3_client.s3_client_abc import S3ClientABC
from src.settings.app_settings import AppSettings
from src.settings.aws_settings import AWSSettings


class S3(S3ClientABC):
    def __init__(self, region_name: str = AWSSettings.REGION_NAME):
        self.s3_client = boto3.client(
            's3',
            region_name=region_name,
            endpoint_url=AWSSettings.ENDPOINT_URL if AppSettings.is_local_environment() else None
        )

    def download_file(self, bucket: str, file_name: str, output_path: str):
        self.s3_client.download_file(bucket, file_name, output_path)

    def upload_binary_file(self, bucket: str, file: bytes, key: str) -> None:
        self.s3_client.upload_fileobj(io.BytesIO(file), bucket, key)
