import aiohttp
import orjson

from linkauto.api.mixins.stub import StubMixin


class TrackMixin(StubMixin):
  async def start_track_mixin(self):
    self.add_response_interceptor(self.set_tracking_headers)
    self.add_response_interceptor(self.generate_network_event)

    # 1. This request retrieves some information necessary for all track requests.
    await self.get(
      'li/track',
      headers={'user-agent': self.get_useragent()},
      default_headers=False
    )

    # 2. Retrieve useless configuration
    await self.get(
      'voyager/api/configuration',
      headers={
        'x-li-track': self.get_track_header(),
        'x-li-lang': self.config.linkedin_stored_data.li_lang,
        'accept': 'application/vnd.linkedin.mobile.deduped+json',
        'user-agent': self.get_useragent(),
        'x-li-page-instance': self.get_page_instance('p_flagship3_background'),
        'csrf-token': self.get_csrf_token(),
        'x-udid': self.config.linkedin_stored_data.li_udid,
        'x-restli-protocol-version': '2.0.0'
      }
    )

  async def generate_network_event(self, _: aiohttp.ClientResponse):
    # TODO: implement
    pass

  async def generate_rum_event(self):
    # TODO: implement
    pass

  async def set_tracking_headers(self, response: aiohttp.ClientResponse):
    headers = response.headers
    self.config.linkedin_stored_data.li_pop = headers.get('x-li-pop', self.config.linkedin_stored_data.li_pop)
    self.config.linkedin_stored_data.li_uuid = headers.get('x-li-uuid', self.config.linkedin_stored_data.li_uuid)
    self.config.linkedin_stored_data.li_proto = headers.get('x-li-proto', self.config.linkedin_stored_data.li_proto)
    self.config.linkedin_stored_data.li_fabric = headers.get('x-li-fabric', self.config.linkedin_stored_data.li_fabric)

  def get_track_header(self) -> str:
    x_li_track = {
      "osName": self.config.device.osName,
      "osVersion": self.config.device.osVersion,
      "model": self.config.device.model,
      "displayDensity": self.config.device.displayDensity,
      "displayWidth": self.config.device.displayWidth,
      "displayHeight": self.config.device.displayHeight,
      "dpi": self.config.device.dpi,
      "deviceType": self.config.device.deviceType,
      "deviceId": self.config.device.deviceId,
      "timezoneOffset": self.config.device.timezoneOffset,
      "timezone": self.config.device.timezone,
      "isAdTrackingLimited": self.config.device.isAdTrackingLimited,
      "appId": self.config.linkedin_app.appId,
      "storeId": self.config.linkedin_app.storeId,
      "clientVersion": self.config.linkedin_app.clientVersion,
      "clientMinorVersion": self.config.linkedin_app.clientMinorVersion,
      "mpName": self.config.linkedin_app.mpName,
      "mpVersion": self.config.linkedin_app.mpVersion
    }
    return orjson.dumps(x_li_track).decode('utf8')
