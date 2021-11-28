from typing import Dict, Any, Optional, List, Callable, Coroutine

import aiohttp
import orjson
import logging

from linkauto.api.enums import TimestampType
from linkauto.api.exceptions import BadRequestException, BadPasswordException
from linkauto.api.mixins.stub import StubMixin

logger = logging.getLogger(__name__)


class HttpMixin(StubMixin):
  _session: aiohttp.ClientSession
  _response_interceptors: List[Callable[[aiohttp.ClientResponse], Coroutine]] = []

  def start_http_mixin(self):
    self._session = aiohttp.ClientSession(cookies={'JSESSIONID': self.generate_csrf_token()})
    self.add_response_interceptor(self._error_handler)

  async def stop_http_mixin(self):
    await self._session.close()

  def add_response_interceptor(self, c: Callable[[aiohttp.ClientResponse], Coroutine]):
    self._response_interceptors.append(c)

  def get_csrf_token(self) -> str:
    return self._session.cookie_jar._cookies['']['JSESSIONID'].coded_value

  def get_lidc_token(self) -> str:
    return self._session.cookie_jar._cookies['linkedin.com']['lidc'].coded_value

  def get_bcookie(self) -> str:
    return self._session.cookie_jar._cookies['linkedin.com']['bcookie'].coded_value

  def get_bscookie(self) -> str:
    return self._session.cookie_jar._cookies['www.linkedin.com']['bscookie'].coded_value

  async def _request(self,
                     url: str,
                     method: str,
                     data: Optional[Any] = None,
                     query_params: Optional[Dict[Any, Any]] = None,
                     headers: Optional[Dict[str, str]] = None,
                     default_headers: bool = True,
                     default_headers_overwrite: bool = False,
                     accept_json: bool = False,
                     page_instance: Optional[str] = None,
                     send_json: bool = False
                     ) -> aiohttp.ClientResponse:
    url = self._prepare_url(url)
    h: Dict[str, str] = self._build_headers(headers, default_headers, default_headers_overwrite)
    query_params = self._build_query_params(query_params or {})
    if page_instance is not None:
      h['x-li-page-instance'] = self.get_page_instance(page_instance)
    if accept_json:
      h['accept'] = 'application/vnd.linkedin.mobile.deduped+json'
    if method.upper() == 'GET':
      if data is not None:
        logger.warning("You're sending a get request with data. The data will be ignored")
      response = await self._session.get(url, headers=headers, params=query_params)
    elif method.upper() == 'POST':
      if send_json:
        data = orjson.dumps(data)
        h['content-type'] = 'application/json'
      response = await self._session.post(url, data=data, headers=headers, params=query_params)
    else:
      raise ValueError('Invalid method: %s', method)
    _ = (await c(response) for c in self._response_interceptors)
    return response

  async def paginate(self, response: Optional[aiohttp.ClientResponse] = None, step: int = 10) -> aiohttp.ClientResponse:
    data = orjson.loads(await response.read())
    if isinstance(data, list):
      raise ValueError("Data is a list. Paginating is not possible.")

    paging = data['paging']
    url = response.real_url.path
    query_params = {
      'count': step,
      'start': paging['start'] + step
    }

    method = response.method
    return await self._request(
      url,
      method,
      query_params=query_params,
      headers={k.decode(): v.decode() for k, v in response.raw_headers},
      default_headers_overwrite=True
    )

  async def get(self,
                url: str,
                query_params: Optional[Dict[Any, Any]] = None,
                headers: Optional[Dict[str, str]] = None,
                default_headers: bool = True,
                accept_json: bool = False,
                page_instance: Optional[str] = None,
                ) -> aiohttp.ClientResponse:
    return await self._request(url, 'GET', query_params=query_params, headers=headers, default_headers=default_headers,
                               accept_json=accept_json, page_instance=page_instance)

  async def post(self, url: str,
                 data: Optional[Any] = None,
                 query_params: Optional[Dict[Any, Any]] = None,
                 headers: Optional[Dict[str, str]] = None,
                 default_headers: bool = True,
                 accept_json: bool = False,
                 page_instance: Optional[str] = None,
                 send_json: bool = False
                 ) -> aiohttp.ClientResponse:
    return await self._request(url, 'POST', query_params=query_params, headers=headers, default_headers=default_headers,
                               accept_json=accept_json, page_instance=page_instance, data=data, send_json=send_json)

  def _build_headers(self, headers: Optional[Dict[str, str]], default_headers: bool, default_headers_overwrite: bool):
    if not default_headers_overwrite:
      return {**(self._get_default_headers() if default_headers else {}), **(headers or {})}
    return {**(headers or {}), **(self._get_default_headers() if default_headers else {})}

  def _build_query_params(self, query_params: Dict[Any, Any]) -> Dict[Any, Any]:
    query_params['nc'] = self.get_timestamp(TimestampType.milliseconds)
    return query_params

  def _get_default_headers(self) -> Dict[str, str]:
    return {
      'user-agent': self.get_useragent(),
      'x-udid': str(self.config.linkedin_stored_data.li_udid),
      'csrf-token': self.get_csrf_token(),
      'x-restli-protocol-version': '2.0.0',
      'x-li-track': self.get_track_header(),
      'x-li-lang': self.config.linkedin_stored_data.li_lang
    }

  def _prepare_url(self, url: str) -> str:
    return "https://www.linkedin.com/" + url.lstrip('/')

  async def _error_handler(self, response: aiohttp.ClientResponse):
    if response.ok:
      return

    try:
      as_json: dict = orjson.loads(await response.read())
    except orjson.JSONDecodeError:
      raise BadRequestException("Unknown error.")

    if isinstance(as_json, list):
      return

    if login_result := as_json.get('login_result'):
      if login_result == 'BAD_PASSWORD':
        raise BadPasswordException()

