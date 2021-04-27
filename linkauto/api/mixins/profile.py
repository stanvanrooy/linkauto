from typing import Optional

import aiohttp

from linkauto.api.mixins.stub import StubMixin


class ProfileMixin(StubMixin):
  async def profile_url_to_id(self, url: str) -> str:
    return url.lstrip('/').replace('in/', '')

  async def profile_get(self, profile_url: Optional[str] = None, id_: Optional[str] = None) -> aiohttp.ClientResponse:
    if not any([profile_url, id_]):
      raise ValueError("Neither an id, or an url has been provided.")

    if id_ is None:
      id_ = await self.profile_url_to_id(profile_url)

    return await self.get(
      f'/voyager/api/voyagerIdentityDashProfiles',
      page_instance='urn:li:page:p_flagship3_profile_view_base',
      accept_json=True,
      query_params={
        'memberIdentity': id_,
        'q': 'memberIdentity',
        'decorationId': 'com.linkedin.voyager.dash.deco.identity.profile.LocalizedProfileWithEntities-68',
      }
    )

  async def profile_get_recommendations(self, given: bool = False, profile_url: Optional[str] = None, id_: Optional[str] = None) -> aiohttp.ClientResponse:
    if not any([profile_url, id_]):
      raise ValueError("neither an id, or an url has been provided.")

    if id_ is None:
      id_ = await self.profile_url_to_id(profile_url)

    return await self.get(
      f'voyager/api/identity/profiles/{id_}/recommendations',
      page_instance='urn:li:page:p_flagship3_profile_view_base',
      accept_json=True,
      query_params={
        'q': 'given' if given else 'received',
      }
    )

  async def profile_get_skills(self, profile_url:  Optional[str] = None, id_: Optional[str] = None) -> aiohttp.ClientResponse:
    if not any([profile_url, id_]):
      raise ValueError("neither an id, or an url has been provided.")

    if id_ is None:
      id_ = await self.profile_url_to_id(profile_url)

    return await self.get(
      f'voyager/api/identity/profiles/{id_}/skills',
      page_instance='urn:li:page:p_flagship3_profile_view_base',
      accept_json=True,
    )

  async def profile_get_connections(self, in_common: bool = False, profile_url:  Optional[str] = None, id_: Optional[str] = None) -> aiohttp.ClientResponse:
    if not any([profile_url, id_]):
      raise ValueError("neither an id, or an url has been provided.")

    if id_ is None:
      id_ = await self.profile_url_to_id(profile_url)

    qp = {'q': 'inCommon' if in_common else 'connections'}
    if not in_common:
      qp['count'] = 10

    return await self.get(
      f'voyager/api/identity/profiles/{id_}/memberConnections',
      page_instance='urn:li:page:p_flagship3_profile_view_base',
      accept_json=True,
      query_params=qp
    )

  async def profile_get_following(self, profile_url:  Optional[str] = None, id_: Optional[str] = None) -> aiohttp.ClientResponse:
    if not any([profile_url, id_]):
      raise ValueError("neither an id, or an url has been provided.")

    if id_ is None:
      id_ = await self.profile_url_to_id(profile_url)

    return await self.get(
      f'voyager/api/identity/profiles/{id_}/following',
      page_instance='urn:li:page:p_flagship3_profile_view_base',
      accept_json=True,
    )

  async def profile_get_contact_info(self, profile_url: Optional[str] = None,
                                    id_: Optional[str] = None) -> aiohttp.ClientResponse:
    if not any([profile_url, id_]):
      raise ValueError("neither an id, or an url has been provided.")

    if id_ is None:
      id_ = await self.profile_url_to_id(profile_url)

    return await self.get(
      f'voyager/api/identity/profiles/{id_}/profileContactInfo',
      page_instance='urn:li:page:p_flagship3_profile_view_base',
      accept_json=True
    )
