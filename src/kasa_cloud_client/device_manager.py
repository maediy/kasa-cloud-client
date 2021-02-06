from uuid import uuid4

from . import devices
from .client import KasaClient
from .device_info import DeviceInfo
from .exceptions import DeviceNotFoundException


class DeviceManager:
    def __init__(
        self,
        user: str,
        passwd: str,
        term_id: str = str(uuid4()),
        enable_cache: bool = True,
    ):
        self.client: KasaClient = KasaClient(user, passwd, term_id)
        self._enable_cache = enable_cache

    def get_devices_info(self) -> DeviceInfo:
        return self.client.devices

    def find_hs100(self, name: str) -> devices.HS100:
        return devices.HS100(
            client=self.client,
            device_info=self.__find_device_info(name),
        )

    def find_lb100(self, name: str) -> devices.LB100:
        return devices.LB100(
            client=self.client,
            device_info=self.__find_device_info(name),
        )

    def find_lb130(self, name: str) -> devices.LB130:
        return devices.LB130(
            client=self.client,
            device_info=self.__find_device_info(name),
        )
        device_info = self.__find_device_info(name)
        return devices.LB130(device_info=device_info, client=self.client)

    def __find_device_info(self, name: str):
        try:
            return next(filter(lambda d: d.alias == name, self.client.devices))
        except StopIteration:
            raise DeviceNotFoundException()
