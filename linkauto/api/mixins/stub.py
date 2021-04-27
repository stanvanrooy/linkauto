from typing import Optional, Dict, Any, Callable, Coroutine

import aiohttp

from linkauto.api.dataclasses_ import Config
from linkauto.api.enums import TimestampType


class _get:
  async def __call__(self,
                url: str,
                query_params: Optional[Dict[Any, Any]] = None,
                headers: Optional[Dict[str, str]] = None,
                default_headers: bool = True,
                accept_json: bool = False,
                page_instance: Optional[str] = None
                ) -> aiohttp.ClientResponse: ...


class _post:
  async def __call__(self, url: str,
                 data: Optional[Any] = None,
                 query_params: Optional[Dict[Any, Any]] = None,
                 headers: Optional[Dict[str, str]] = None,
                 default_headers: bool = True,
                 accept_json: bool = False,
                 page_instance: Optional[str] = None,
                 send_json: bool = False
                 ) -> aiohttp.ClientResponse: ...


class _get_useragent:
  def __call__(self) -> str: ...


class _get_page_instance:
  def __call__(self, page: str) -> str: ...


class _get_timestamp:
  @staticmethod
  def __call__(d: TimestampType) -> int: ...


class _generate_csrf_token:
  def __call__(self) -> str: ...


class _get_csrf_token:
  def __call__(self) -> str: ...


class _add_response_interceptor:
  def __call__(self, c: Callable[[aiohttp.ClientResponse], Coroutine]): ...


class _get_track_header:
  def __call__(self) -> str: ...


class _get_lidc_token:
  def __call__(self) -> str: ...


class _get_bcookie:
  def __call__(self) -> str: ...


class _get_bscookie:
  def __call__(self) -> str: ...


class _profile_url_to_id:
  async def __call__(self, url: str) -> str: ...


class _get_tracking_id:
  def __call__(self) -> str: ...


class StubMixin:
  username: str
  password: str
  config: Config
  get: _get
  post: _post
  get_useragent: _get_useragent
  get_page_instance: _get_page_instance
  get_timestamp: _get_timestamp
  generate_csrf_token: _generate_csrf_token
  get_csrf_token: _get_csrf_token
  add_response_interceptor: _add_response_interceptor
  get_track_header: _get_track_header
  get_lidc_token: _get_lidc_token
  get_bcookie: _get_bcookie
  get_bscookie: _get_bscookie
  profile_url_to_id: _profile_url_to_id
  get_tracking_id: _get_tracking_id
