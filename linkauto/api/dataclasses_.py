import dataclasses
import uuid
from typing import Type


@dataclasses.dataclass
class Device:
  osName: str
  osVersion: str
  model: str
  displayDensity: float
  displayWidth: int
  displayHeight: int
  dpi: str
  deviceType: str
  timezoneOffset: int
  timezone: str
  isAdTrackingLimited: bool
  androidVersion: str
  region: str
  cronetVersion: str
  deviceId: str = None


@dataclasses.dataclass
class LinkedinApp:
  clientVersion: str
  clientMinorVersion: int
  storeId: str
  appId: str
  mpName: str
  mpVersion: str


@dataclasses.dataclass
class LinkedinStoredData:
  li_lang: str
  li_udid: uuid.UUID = dataclasses.field(default_factory=lambda: str(uuid.uuid4))
  li_fabric: str = None
  li_pop: str = None
  li_proto: str = None
  li_uuid: str = None


@dataclasses.dataclass
class Config:
  device: Type[Device]
  linkedin_app: Type[LinkedinApp]
  linkedin_stored_data: LinkedinStoredData

