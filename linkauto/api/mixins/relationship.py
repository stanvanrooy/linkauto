from typing import Optional

import aiohttp

from linkauto.api.enums import ConnectionInviteType
from linkauto.api.mixins.stub import StubMixin


class RelationshipMixin(StubMixin):
  async def relationship_invitation_create(self,
                                           message: Optional[str] = None,
                                           profile_url: Optional[str] = None,
                                           id_: Optional[str] = None
                                           ) -> aiohttp.ClientResponse:
    if not any([profile_url, id_]):
      raise ValueError("Neither an id, or an url has been provided.")

    if id_ is None:
      id_ = await self.profile_url_to_id(profile_url)

    data = {
      'trackingId': self.get_tracking_id(),
      'invitee': {
        'com.linkedin.voyager.growth.invitation.InviteeProfile': {
          'profileId': id_
        }
      },
    }
    if message is not None:
      data['message'] = message

    return await self.post(
      f'/voyager/api/voyagerGrowthNormInvitations',
      data=data,
      page_instance='urn:li:page:p_flagship3_profile_view_base',
      accept_json=True,
      send_json=True
    )

  async def relationship_invitation_get(self, type_: ConnectionInviteType):
    url = "/voyager/api/relationships/invitationViews"
    if type_ == type_.SENT:
      url = "/voyager/api/relationships/sentInvitationViewsV2"
    return await self.get(
      url,
      query_params={
        'q': type_.value,
        'invitationType': 'CONNECTION',
        'start': 0,
        'count': 10
      },
      accept_json=True,
      page_instance='urn:li:page:p_flagship3_people_sent_invitations'
    )
