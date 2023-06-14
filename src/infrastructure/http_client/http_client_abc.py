from abc import ABC, abstractmethod
from typing import Tuple, Union, Optional

from src.infrastructure.model.pydantic.http_client.http_client_response_model import HttpClientResponseModel


class HttpClientABC(ABC):
    NotImplementedErrorMessage = 'Method {} not implemented!'

    async def get(
        self,
        url: str,
        headers: dict,
        timeout: float = 25,
        alias: str = None,
        basic_auth: Optional[Tuple[str, str]] = None,
        verify_ssl_certificate: Optional[bool] = True,
        query_params: Optional[dict] = None,
        follow_redirects: Optional[bool] = True,
        **kwargs
    ) -> HttpClientResponseModel:
        raise NotImplementedError(self.NotImplementedErrorMessage.format('get'))

    async def post(
        self,
        url: str,
        headers: dict,
        body: Union[dict, str],
        timeout: float = 25,
        alias: str = None,
        basic_auth: Optional[Tuple[str, str]] = None,
        verify_ssl_certificate: Optional[bool] = True,
        follow_redirects: Optional[bool] = True,
        **kwargs
    ) -> HttpClientResponseModel:
        raise NotImplementedError(self.NotImplementedErrorMessage.format('post'))

    async def put(
        self,
        url: str,
        headers: dict,
        body: Union[dict, str],
        timeout: float = 25,
        alias: str = None,
        basic_auth: Optional[Tuple[str, str]] = None,
        verify_ssl_certificate: Optional[bool] = True,
        follow_redirects: Optional[bool] = True,
        **kwargs
    ) -> HttpClientResponseModel:
        raise NotImplementedError(self.NotImplementedErrorMessage.format('put'))
