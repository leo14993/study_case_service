from abc import ABC


class S3ClientABC(ABC):
    def download_file(self, bucket: str, file_name: str, output_path: str):
        raise NotImplementedError('S3 client download file not implemented')

    def upload_binary_file(self, bucket: str, file: bytes, key: str) -> None:
        raise NotImplementedError('S3 client upload file not implemented')
