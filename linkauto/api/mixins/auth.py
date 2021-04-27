import aiohttp

from linkauto.api.enums import TimestampType
from linkauto.api.mixins.stub import StubMixin


class AuthMixin(StubMixin):
  async def login(self) -> aiohttp.ClientResponse:
    return await self.post(
      'uas/authenticate',
      data={
        'session_key': self.username,
        'session_password': self.password,
        'client_enabled_features': 'ANDROID_NATIVE_CAPTCHA',
        'rememberMeOptIn': 'false',
        'JSESSIONID': self.get_csrf_token(),
        'lidc': self.get_lidc_token(),
        'bcookie': self.get_bcookie(),
        'bscookie': self.get_bscookie(),
        'lang': f'v=2&lang={self.config.linkedin_stored_data.li_lang}',
      },
      headers={
        'x-li-user-agent': f'LIAuthLibrary:0.0.3 {self.config.linkedin_app.appId}:{self.config.linkedin_app.clientVersion}'
                           f' {self.config.device.model}:{self.config.device.androidVersion}',
        'user-agent': 'ANDROID OS'
      }
    )

  async def logout(self) -> aiohttp.ClientResponse:
    await self.post(
      'voyager/api/pushRegistration',
      query_params={
        'action': 'deregister',
      }, headers={
        'x-li-user-agent': f'LIAuthLibrary:0.0.3 {self.config.linkedin_app.appId}:{self.config.linkedin_app.clientVersion}'
                           f' {self.config.device.model}:{self.config.device.androidVersion}'
      }
    )
    return await self.post(
      'uas/directLogout',
      data={
        'rememberMeOptIn': 'false',
        'JSESSIONID': self.get_csrf_token(),
        'lang': f'v=2&lang={self.config.linkedin_stored_data.li_lang}',
        'logout_reason': 'USER_INITIATED'
      },
      headers={
        'x-li-user-agent': f'LIAuthLibrary:0.0.3 {self.config.linkedin_app.appId}:{self.config.linkedin_app.clientVersion}'
                           f' {self.config.device.model}:{self.config.device.androidVersion}'
      }
    )
