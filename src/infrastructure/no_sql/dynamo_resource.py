from typing import List, Dict, Optional, Union

import boto3

from src.settings.app_settings import AppSettings
from src.settings.aws_settings import AWSSettings


class DynamoResource:

    def __init__(self,
                 table: str,
                 region_name: str = AWSSettings.REGION_NAME):
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=region_name,
            endpoint_url=AWSSettings.ENDPOINT_URL if AppSettings.is_local_environment() else None
        )

        self.table = self.dynamodb.Table(table)

    async def get_all(self) -> List[Dict]:
        response = self.table.scan()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        return data

    async def get_by_id(self, value: Union[str, int], id_name: str = 'id') -> Optional[Dict]:
        response = self.table.get_item(Key={id_name: value})

        return response.get('Item')

    async def save(self, payload: Dict, id_name: str = 'id') -> Optional[Dict]:
        self.table.put_item(Item=payload)
        return await self.get_by_id(payload[id_name])

    async def delete(self, value: Union[str, int], id_name: str = 'id') -> None:
        self.table.delete_item(Key={id_name: value})
