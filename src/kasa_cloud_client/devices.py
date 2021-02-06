import json
from abc import ABC, abstractmethod
from typing import Optional

from . import states
from .client import KasaClient
from .device_info import DeviceInfo
from .exceptions import UnmatchedDeviceException


class Device(ABC):
    def __init__(self, device_info: DeviceInfo, client: KasaClient):
        self._device_info = device_info
        self._client = client
        if not self._validate_device_info():
            UnmatchedDeviceException()

    @property
    @abstractmethod
    def SERVICE_NAME(self) -> str:
        pass

    @abstractmethod
    def _validate_device_info(self):
        """
        Validate if the device_info is an appropriate type of the class.
        If not, raise UnmatchedDeviceException.
        """
        pass

    def passthrogh(self, cmd) -> dict:
        res = self._client.passthrogh(
            self._device_info, json.dumps({self.SERVICE_NAME: cmd})
        )
        return res[self.SERVICE_NAME]


class HS100(Device):
    @property
    def SERVICE_NAME(self) -> str:
        return "system"

    def _validate_device_info(self):
        if "plug" not in self._device_info.device_type.lower():
            raise UnmatchedDeviceException()

    def _get_state(self) -> dict:
        cmd = "get_sysinfo"
        res = self.passthrogh({cmd: None})
        return res[cmd]

    def get_state(self) -> states.HS100State:
        return states.HS100State.from_dict(self._get_state())

    def _set_state(self, state: dict) -> dict:
        cmd = "set_relay_state"
        self.passthrogh({cmd: state})

    def set_state(
        self,
        relay_state: int,
    ):
        self._set_state({"state": relay_state})

    def turn_on(self):
        self.set_state(1)

    def turn_off(self):
        self.set_state(0)


class LB100(Device):
    @property
    def SERVICE_NAME(self) -> str:
        return "smartlife.iot.smartbulb.lightingservice"

    def _validate_device_info(self):
        if "bulb" not in self._device_info.device_type.lower():
            raise UnmatchedDeviceException()

    def _get_state(self) -> dict:
        cmd = "get_light_state"
        res = self.passthrogh({cmd: {}})
        return res[cmd]

    def get_state(self) -> states.LB100State:
        return states.LB100State.from_dict(self._get_state())

    def _set_state(self, state: dict) -> dict:
        cmd = "transition_light_state"
        self.passthrogh({cmd: state})

    def set_state(self, on_off: int):
        res = self._set_state({"on_off": on_off})

    def turn_on(self):
        self.set_state(1)

    def turn_off(self):
        self.set_state(0)


class LB130(LB100):
    def _validate_device_info(self):
        super()._validate_device_info()
        if "130" not in self._device_info.device_model:
            raise UnmatchedDeviceException()

    def set_state(
        self,
        on_off: int,
        brightness: Optional[int] = None,
        hue: Optional[int] = None,
        saturation: Optional[int] = None,
        color_temp: Optional[int] = None,
    ):
        self._set_state(
            {
                "on_off": on_off,
                "brightness": brightness,
                "hue": hue,
                "saturation": saturation,
                "color_temp": color_temp,
            }
        )

    def get_state(self) -> states.LB130State:
        res = self._get_state()
        return states.LB130State.from_dict(res)
