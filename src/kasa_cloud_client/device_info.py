from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DeviceInfo:
    fw_ver: str
    alias: str
    status: int
    device_id: str
    role: str
    device_mac: str
    device_name: str
    device_type: str
    device_model: str
    app_server_url: str
