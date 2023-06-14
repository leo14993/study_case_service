from splitio import get_factory
from splitio.client.client import Client
from typing import Union, Dict, List, Optional

from src.settings.external_services import SplitIOSettings


class SplitIOClient:
    configuration = {
        'impressionsMode': SplitIOSettings.IMPRESSIONS_MODE,
        'connectionTimeout': SplitIOSettings.CONNECTION_TIMEOUT,
        'readTimeout': SplitIOSettings.READ_TIMEOUT,
    }
    split_io_client: Client

    def __init__(self) -> None:
        self.factory = get_factory(
            api_key=SplitIOSettings.SPLIT_IO_API_KEY,
            config=self.configuration
        )

        self.factory.block_until_ready(SplitIOSettings.TIME_OUT_SPLIT_IO)

        self.split_io_client = self.factory.client()

    async def get_feature(self,
                          id: str,
                          split: str,
                          attrs: Optional[Dict],
                          convert_to_boolean: bool = False) -> Union[str, bool]:
        treatment = self.split_io_client.get_treatment(id, split, attrs)

        return self._convert_to_boolean(treatment) if convert_to_boolean else treatment

    async def get_features(self,
                           id: str,
                           splits: List[str],
                           attrs: Optional[Dict] = None) -> Dict:
        treatments = self.split_io_client.get_treatments(id, splits, attrs)

        return treatments

    @staticmethod
    def _convert_to_boolean(treatment: str) -> bool:
        return treatment == 'on'
