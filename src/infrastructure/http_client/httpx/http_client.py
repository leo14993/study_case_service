from http import HTTPStatus

import httpx
import json

from typing import Tuple, Union, Optional

from src.infrastructure.http_client.http_client_abc import HttpClientABC
from src.infrastructure.model.pydantic.http_client.http_client_response_model import HttpClientResponseModel
from src.infrastructure.model.pydantic.http_client.request_model import Request


class HttpClient(HttpClientABC):

    @classmethod
    async def get(
        cls,
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
        try:
            async with httpx.AsyncClient(verify=verify_ssl_certificate) as client:
                response = await client.get(
                    url=url,
                    headers=headers,
                    params=query_params,
                    timeout=timeout,
                    auth=basic_auth,
                    follow_redirects=follow_redirects,
                    **kwargs
                )
            response_model = cls._convert_response(response=response, alias=alias)
        except httpx.TimeoutException as e:
            response_model = cls._convert_response_timeout(error=e, timeout=timeout, alias=alias)
        return response_model

    @classmethod
    async def post(
        cls,
        url: str,
        headers: dict,
        body: Union[dict, str],
        timeout: float = 25,
        alias: str = None,
        basic_auth: Optional[Tuple[str, str]] = None,
        verify_ssl_certificate: Optional[bool] = True,
        **kwargs
    ) -> HttpClientResponseModel:
        try:
            params = cls._request_params(
                url=url,
                headers=headers,
                body=body,
                timeout=timeout,
                basic_auth=basic_auth,
                **kwargs
            )
            async with httpx.AsyncClient(verify=verify_ssl_certificate) as client:
                response = await client.post(**params)
            response_model = cls._convert_response(response=response, alias=alias)
        except httpx.TimeoutException as e:
            response_model = cls._convert_response_timeout(error=e, timeout=timeout, alias=alias)
        return response_model

    @classmethod
    async def put(
        cls,
        url: str,
        headers: dict,
        body: Union[dict, str],
        timeout: float = 25,
        alias: str = None,
        basic_auth: Optional[Tuple[str, str]] = None,
        verify_ssl_certificate: Optional[bool] = True,
        **kwargs
    ) -> HttpClientResponseModel:
        try:
            params = cls._request_params(
                url=url,
                headers=headers,
                body=body,
                timeout=timeout,
                basic_auth=basic_auth,
                **kwargs
            )
            async with httpx.AsyncClient(verify=verify_ssl_certificate) as client:
                response = await client.put(**params)
            response_model = cls._convert_response(response=response, alias=alias)
        except httpx.TimeoutException as e:
            response_model = cls._convert_response_timeout(error=e, timeout=timeout, alias=alias)
        return response_model

    @staticmethod
    def _request_params(url: str,
                        headers: dict,
                        body: Union[dict, str],
                        timeout: float = 25,
                        basic_auth: Tuple[str, str] = None,
                        **kwargs) -> dict:
        params = {
            'url': url,
            'headers': headers,
            'timeout': timeout,
            'auth': basic_auth,
            **kwargs
        }
        if isinstance(body, dict) or isinstance(body, list):
            params['json'] = body
        else:
            params['data'] = body
        return params

    @staticmethod
    def _convert_response(response: httpx.Response, alias: str = None) -> HttpClientResponseModel:
        process_time_seconds = response.elapsed.total_seconds()
        event_request = Request(
            method=response.request.method,
            url=str(response.request.url),
            status_code=response.status_code,
            process_time=process_time_seconds,
            alias=alias
        )
        response_model = HttpClientResponseModel(
            headers=response.headers,
            status_code=response.status_code,
            payload=response.json(),
            response_text=response.text,
            url=str(response.request.url),
            method=response.request.method,
            process_time=process_time_seconds,
            event_request=event_request
        )
        return response_model

    @staticmethod
    def _convert_response_timeout(error: httpx.TimeoutException, timeout: float,
                                  alias: str = None) -> HttpClientResponseModel:
        status_code = HTTPStatus.REQUEST_TIMEOUT.value
        class_name = type(error).__name__
        body_json = {
            'error': HTTPStatus.REQUEST_TIMEOUT.description,
            'type': class_name
        }
        event_request = Request(
            method=error.request.method,
            url=str(error.request.url),
            status_code=status_code,
            process_time=timeout,
            alias=alias
        )
        response_model = HttpClientResponseModel(
            headers=None,
            status_code=status_code,
            response_text=json.dumps(body_json),
            url=str(error.request.url),
            method=error.request.method,
            process_time=timeout,
            event_request=event_request
        )
        return response_model
