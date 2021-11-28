import asyncio
from typing import Type

from linkauto.api.constants import Linkedin_41588_146600, GooglePixelUS
from linkauto.api.dataclasses_ import Device, LinkedinStoredData, LinkedinApp, Config
from linkauto.api.mixins.auth import AuthMixin
from linkauto.api.mixins.helper import HelperMixin
from linkauto.api.mixins.http import HttpMixin
from linkauto.api.mixins.profile import ProfileMixin
from linkauto.api.mixins.relationship import RelationshipMixin
from linkauto.api.mixins.track import TrackMixin


class ApiClient(HttpMixin, TrackMixin, AuthMixin, HelperMixin, ProfileMixin, RelationshipMixin):
  def __init__(self, username: str, password: str, linkedin_app: Type[LinkedinApp], device: Type[Device]):
    self.config = Config(device, linkedin_app, LinkedinStoredData(device.region))
    self.username = username
    self.password = password
    self.start_http_mixin()

  async def init(self):
    await self.start_track_mixin()

  async def stop(self):
    await self.stop_http_mixin()

