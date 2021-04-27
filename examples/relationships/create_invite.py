import asyncio

import orjson

from linkauto.api.constants import Linkedin_41588_146600, GooglePixelUS
from linkauto.api.client import ApiClient
from linkauto.api.enums import ConnectionInviteType


async def main():
  client = ApiClient("username", "password", Linkedin_41588_146600, GooglePixelUS)
  await client.init()
  await client.login()
  response = await client.relationship_invitation_create(profile_url="/in/stan-van-rooy")


if __name__ == '__main__':
  asyncio.run(main())
