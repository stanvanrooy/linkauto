import asyncio

import orjson

from linkauto.api.constants import Linkedin_41588_146600, GooglePixelUS
from linkauto.api.client import ApiClient


async def main():
  client = ApiClient("username", "password", Linkedin_41588_146600, GooglePixelUS)
  await client.init()
  await client.login()
  response = await client.profile_get(profile_url='/in/stan-van-rooy')
  profile = orjson.loads(await response.read())


if __name__ == '__main__':
  asyncio.run(main())
