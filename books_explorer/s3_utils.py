import boto3
from django.conf import settings


class CustomS3:

    def __init__(self, bucket_name: str = 'myshinybuckket'):
        try:
            self.s3 = boto3.client('s3', **self.credentials)
            self.bucket_name = bucket_name

        except Exception as e:
            raise ("Can't authenticate", e)
        finally:
            pass
            # TODO logging

    @property
    def credentials(self):
        return {
            'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY
        }

    def upload_file(self, file: str, file_name: str):
        try:
            self.s3.upload_file(file, self.bucket_name, file_name)
        except Exception as e:
            raise e
            # TODO logging

    def build_url_for_file(self, file_name: str) -> str:
        # https://myshinybuckket.s3.eu-west-2.amazonaws.com/285995bc-5e9a-4f2f-924c-70281508aa0b.csv
        return f'https://{self.bucket_name}s3.eu-west-2.amazonaws.com/{file_name}'

    def get_file(self, file_name: str):
        try:
            return self.s3.get_object(Bucket=self.bucket_name, Key=file_name)
        except Exception as e:
            raise e
            # TODO logging



