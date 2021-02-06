import json
from dataclasses import dataclass
from typing import Optional

import requests
from dataclasses_json import LetterCase, dataclass_json

from .device_info import DeviceInfo


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Params:
    term_id: str
    token: Optional[str] = None
    app_name: str = "Kasa_Android"
    ospf: str = "Android+6.0.1"
    net_type: str = "wifi"
    locale: str = "ja_JP"

    def to_dict() -> dict:
        pass


class KasaClient:
    API_ENDPOINT = "https://wap.tplinkcloud.com"
    HEADERS = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; A0001 Build/M4B30X)",
        "Content-Type": "application/json",
    }

    def __init__(self, user: str, passwd: str, term_id: str, enable_cache: bool = True):
        self.__user = user
        self.__passwd = passwd
        self.__enable_cache = enable_cache
        self.term_id = term_id
        self.token = self.login()
        self.__cached_devices = self.get_devices() if enable_cache else []

    def login(self) -> str:
        res = requests.post(
            self.API_ENDPOINT,
            headers=self.HEADERS,
            params=Params(term_id=self.term_id).to_dict(),
            json={
                "method": "login",
                "url": self.API_ENDPOINT,
                "params": {
                    "appType": "Kasa_Android",
                    "cloudPassword": self.__passwd,
                    "cloudUserName": self.__user,
                    "terminalUUID": self.term_id,
                },
            },
        )
        res.raise_for_status()

        return res.json()["result"]["token"]

    def get_devices(self) -> DeviceInfo:
        res = requests.post(
            self.API_ENDPOINT,
            headers=self.HEADERS,
            params=Params(term_id=self.term_id, token=self.token).to_dict(),
            json={"method": "getDeviceList"},
        )
        res.raise_for_status()

        return list(map(DeviceInfo.from_dict, res.json()["result"]["deviceList"]))

    def passthrogh(self, device_info: DeviceInfo, cmd: str):
        res = requests.post(
            device_info.app_server_url,
            headers=self.HEADERS,
            params=Params(term_id=self.term_id, token=self.token).to_dict(),
            json={
                "method": "passthrough",
                "params": {"deviceId": device_info.device_id, "requestData": cmd},
            },
        )
        res.raise_for_status()
        return json.loads(res.json()["result"]["responseData"])

    @property
    def devices(self) -> DeviceInfo:
        if self.__enable_cache:
            return self.__cached_devices
        return self.get_devices()
