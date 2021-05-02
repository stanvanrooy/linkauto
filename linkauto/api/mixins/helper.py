import base64
import random
import uuid

from linkauto.api.enums import TimestampType

import time

from linkauto.api.mixins.stub import StubMixin


class HelperMixin(StubMixin):
  @staticmethod
  def get_timestamp(d: TimestampType) -> int:
    """Retrieve the current timestamp.
    Args:
        d: controls the precision of the returned timestamp.
    Returns: the current timestamp.
    """
    return int(str(time.time_ns())[:d.value])

  def get_useragent(self) -> str:
    return f"{self.config.linkedin_app.appId}/{self.config.linkedin_app.clientMinorVersion} " \
           f"(Linux; U; {self.config.device.androidVersion}; {self.config.device.region}; " \
           f"{self.config.device.model}; Build/NMF26Q; Cronet/{self.config.device.cronetVersion})"

  def get_tracking_id(self) -> str:
    return base64.b64encode(uuid.uuid4().bytes).decode()

  def get_page_instance(self, page: str) -> str:
    return f"{page};{base64.b64encode(uuid.uuid4().bytes)}"

  def generate_csrf_token(self) -> str:
    r = list(str(self.get_timestamp(TimestampType.nanoseconds)))
    random.shuffle(r)
    return f'ajax:{"".join(r)}'
