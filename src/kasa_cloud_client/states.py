from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional

@dataclass_json
@dataclass
class HS100State:
    relay_state: int


@dataclass_json
@dataclass
class LB100State:
    on_off: int


@dataclass
class LB130State(LB100State):
    brightness: Optional[int] = None
    hue: Optional[int] = None
    saturation: Optional[int] = None
    color_temp: Optional[int] = None
