from decouple import config


class AWSSettings:
    ENDPOINT_URL = config('AWS_ENDPOINT_URL', default='http://localhost:8000')
    REGION_NAME = config('AWS_REGION_NAME', default='us-east-1')
    DYNAMO_TABLE_NAME = config('DYNAMO_TABLE_NAME', default='my-table')

