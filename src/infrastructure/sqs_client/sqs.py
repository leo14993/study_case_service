import json

import boto3

from uuid import uuid4
from typing import List, Optional

from src.infrastructure.model.pydantic.sqs.sqs_message_model import SqsReceivedMessageModel, SqsMessageModel
from src.infrastructure.sqs_client.sqs_client_abc import SqsClientABC
from src.settings.app_settings import AppSettings
from src.settings.aws_settings import AWSSettings


class SQS(SqsClientABC):

    def __init__(self, region_name: str = AWSSettings.REGION_NAME):
        self.sqs_client = boto3.client(
            'sqs',
            region_name=region_name,
            endpoint_url=AWSSettings.ENDPOINT_URL if AppSettings.is_local_environment() else None
        )

    def receive_message(self, queue_url: str, max_messages: int = 10) -> List[SqsReceivedMessageModel]:
        queue_messages = self.sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_messages
        )
        messages = []
        if 'Messages' in queue_messages and len(queue_messages['Messages']) >= 1:
            for message in queue_messages['Messages']:
                messages.append(SqsReceivedMessageModel(
                    data=json.loads(message['Body']),
                    receipt_handle=message['ReceiptHandle']
                ))

        return messages

    def send_message(self, sqs_message: SqsMessageModel, queue_url: str, deduplication_id: Optional[str]) -> None:

        message_body = sqs_message.json()
        send_message_parameters = {
            'QueueUrl': queue_url,
            'MessageBody': message_body,
        }

        if '.fifo' in queue_url:
            message_group_id = str(uuid4())

            send_message_parameters.update({
                'MessageGroupId': message_group_id,
            })

        if deduplication_id:
            send_message_parameters.update({
                'MessageDeduplicationId': deduplication_id,
            })

        send_message_parameters.update({
            'DelaySeconds': 0,
            'MessageAttributes': {}
        })

        self.sqs_client.send_message(
            **send_message_parameters
        )

    def delete_message(self, receipt_handle: str, queue_url: str) -> None:
        self.sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )

    def delete_all_messages(self, queue_url: str) -> None:
        self.sqs_client.purge_queue(
            QueueUrl=queue_url
        )
