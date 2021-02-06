# Introduction
This package can control your TP-Link smart plugs or smart bulbs remotely using TP-Link cloud service.

# Installation
```bash
poetry build
pip install dist/kasa-cloud-client-*.tar.gz
```

# Usage
## Authenticate
```python
from kasa_cloud_client import DeviceManager

device_manager = KasaDeviceManager(
    user="YOUR_USER_ID (e.g. foobar@example.com",
    passwd="YOUR_PASSOWRD",
    # term_id: "YOUR_TERMINAL_ID (not required",
)
```

## Fetch registerd devices
```python
device_manager.get_devices_info()
```

## Control Your devices
### Smartplugs (HS10x)
```python
plug = device_manager.find_hs100("YOUR_DEVICE_NAME")

# get current state
plug.get_state()

# turn on
plug.turn_on()

# turn off
plug.turn_off()
```

### Smartbulbs (LB100/130, KL130)
```python
bulb = device_manager.find_lb100("YOUR_DEVICE_NAME")

# get current state
plug.get_state()

# turn on
plug.turn_on()

# turn off
plug.turn_off()
```

If you have an LB130 or KL130, use this:
```python
from kasa_cloud_client.states import LB130State
bulb = device_manager.find_lb130("YOUR_DEVICE_NAME")

# get current state
state = plug.get_state()

# change brightness
plug.set_state(on_off=1, brightness=50, color_temp=2700)

# or you can use the result of get_state to update state
state.brightness = 50
plug.set_state(**state.to_dict())
```
The five parameters for LB130 or KL130 are:
- on_off: 1 on, 0 off
- brightness: 0-100
- hue: 0-360
- saturation: 0-100
- color_temp: 2500-9000

# Requires
python 3.8 or higher
