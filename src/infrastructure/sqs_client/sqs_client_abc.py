from abc import ABC
from typing import Optional

from src.infrastructure.model.pydantic.sqs.sqs_message_model import SqsMessageModel


class SqsClientABC(ABC):

    def configure(self, queue_url: str, region_name: str) -> None:
        raise NotImplementedError

    def send_message(self, sqs_message: SqsMessageModel, queue_url: str, deduplication_id: Optional[str]) -> None:
        raise NotImplementedError('SQS client send message not implemented')
