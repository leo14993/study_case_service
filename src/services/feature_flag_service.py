from typing import Dict

import inject

from src.infrastructure.split_io.split_io_client import SplitIOClient


class FeatureFlagService:
    split_io_client: SplitIOClient = inject.attr(SplitIOClient)

    async def get_feature_flag_treatments(self, payload: Dict) -> Dict:

        attributes = {
            'myVersion': payload['myVersion'],
            'reason': payload['reason'],

        }

        splits = [
            'myFirstFeatureFlag',
            'mySecondFeatureFlags',
        ]

        return await self.split_io_client.get_features(payload['user_id'], splits, attributes)