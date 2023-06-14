import datetime
from http import HTTPStatus

import requests

from typing import Tuple, Union, Optional

from requests.exceptions import ReadTimeout

from src.infrastructure.http_client.http_client_abc import HttpClientABC
from src.infrastructure.model.pydantic.http_client.http_client_response_model import HttpClientResponseModel
from src.infrastructure.model.pydantic.http_client.request_model import Request


class HttpClient(HttpClientABC):
    async def get(
        self,
        url: str,
        headers: dict,
        timeout: float = 25,
        alias: str = None,
        basic_auth: Optional[Tuple[str, str]] = None,
        verify_ssl_certificate: Optional[bool] = True,
        follow_redirects: Optional[bool] = True,
        **kwargs
    ) -> HttpClientResponseModel:
        try:
            response = requests.get(
                url=url,
                headers=headers,
                timeout=timeout,
                auth=basic_auth,
                verify=verify_ssl_certificate,
                **kwargs
            )
            response_model = self._convert_response(response=response, alias=alias)
        except ReadTimeout as e:
            response_model = self._convert_response_timeout(error=e, timeout=timeout, alias=alias)
        return response_model

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
        try:
            params = self._request_params(
                url=url,
                headers=headers,
                body=body,
                timeout=timeout,
                basic_auth=basic_auth,
                verify=verify_ssl_certificate,
                follow_redirects=follow_redirects,
                **kwargs
            )
            response = requests.post(**params)
            response_model = self._convert_response(response=response, alias=alias)
        except ReadTimeout as e:
            response_model = self._convert_response_timeout(error=e, timeout=timeout, alias=alias)
        return response_model

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
        try:
            params = self._request_params(
                url=url,
                headers=headers,
                body=body,
                timeout=timeout,
                basic_auth=basic_auth,
                verify=verify_ssl_certificate,
                follow_redirects=follow_redirects,
                **kwargs
            )
            response = requests.put(**params)
            response_model = self._convert_response(response=response, alias=alias)
        except ReadTimeout as e:
            response_model = self._convert_response_timeout(error=e, timeout=timeout, alias=alias)
        return response_model

    @staticmethod
    def _request_params(url: str,
                        headers: dict,
                        body: Union[dict, str],
                        timeout: float = 25,
                        verify: bool = True,
                        basic_auth: Tuple[str, str] = None,
                        **kwargs) -> dict:
        params = {
            'url': url,
            'headers': headers,
            'timeout': timeout,
            'auth': basic_auth,
            'verify': verify,
            **kwargs
        }
        if isinstance(body, dict):
            params['json'] = body
        else:
            params['data'] = body
        return params

    def _convert_response(self, response: requests.Response, alias: str = None) -> HttpClientResponseModel:
        process_time_seconds = response.elapsed.total_seconds()

        event_request = Request(
            method=response.request.method,
            url=response.request.url,
            status_code=response.status_code,
            process_time=process_time_seconds,
            alias=alias
        )
        response_model = HttpClientResponseModel(
            headers=response.headers,
            status_code=response.status_code,
            payload=response.json(),
            response_text=response.text,
            url=response.request.url,
            method=response.request.method,
            process_time=process_time_seconds,
            event_request=event_request
        )
        return response_model

    @staticmethod
    def _convert_response_timeout(error: ReadTimeout, timeout: float, alias: str = None) -> HttpClientResponseModel:
        status_code = HTTPStatus.REQUEST_TIMEOUT.value
        body_json = f"{'error': {HTTPStatus.REQUEST_TIMEOUT.description}}"
        event_request = Request(
            method=error.request.method,
            url=error.request.url,
            status_code=status_code,
            process_time=timeout,
            alias=alias
        )
        response_model = HttpClientResponseModel(
            headers=None,
            status_code=status_code,
            response_text=body_json,
            url=error.request.url,
            method=error.request.method,
            process_time=timeout,
            event_request=event_request
        )
        return response_model

    @staticmethod
    def _timedelta_to_millisecond(time: datetime.timedelta) -> int:
        seconds_in_milli = time.seconds * 1000
        microseconds_in_milli = time.microseconds / 1000
        time_in_mili = seconds_in_milli + int(microseconds_in_milli)
        time_in_mili_str = str(time_in_mili)[0:4]
        return int(time_in_mili_str)

