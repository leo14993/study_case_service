__version__ = '1.0.0'

import inject

from src.infrastructure.http_client.httpx.http_client import HttpClient
from src.infrastructure.no_sql.dynamo_resource import DynamoResource
from src.infrastructure.split_io.split_io_client import SplitIOClient
from src.settings.aws_settings import AWSSettings


def configure_split_io_client(binder):
    binder.bind_to_constructor(
        SplitIOClient,
        lambda: SplitIOClient()
    )


def configure_http_client(binder):
    binder.bind_to_provider(
        HttpClient,
        lambda: HttpClient()
    )


def configure_dynamo_resource(binder):
    binder.bind_to_constructor(
        DynamoResource,
        lambda: DynamoResource(AWSSettings.DYNAMO_TABLE_NAME)
    )


adapter_binders = [
]


def configure(binder):
    configure_http_client(binder)
    configure_split_io_client(binder)
    configure_dynamo_resource(binder)


inject.configure(configure)
