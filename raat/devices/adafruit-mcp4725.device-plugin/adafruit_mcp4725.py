import logging

from pathlib import Path

from collections import namedtuple

from yapsy.IPlugin import IPlugin

from raat.types import DeviceSource, DeviceInclude, LibraryInclude

from raat.devices.generic_device import GenericDevice, GenericDevicePlugin
from raat.types import Setting

THIS_PATH = Path(__file__).parent


class Adafruit_MCP4725RAAT(
    GenericDevice, namedtuple("Adafruit_MCP4725RAAT", ["name", "i2c_address", "default", "min", "max"])
):

    __slots__ = ()

    sources = (DeviceSource(THIS_PATH, "adafruit-mcp4725.cpp"), )

    includes = (
        LibraryInclude("Adafruit_MCP4725.h"),
        DeviceInclude(THIS_PATH, "adafruit-mcp4725.hpp")
    )

    @property
    def required_libraries(self):
        return ["Adafruit MCP4725"]

    @property
    def setup(self):
        return "{name}.setup();".format(name=self.cname())

    @property
    def directory(self):
        return THIS_PATH

    @property
    def declarations(self):
        return "static Adafruit_MCP4725RAAT {name} = Adafruit_MCP4725RAAT(0x{addr:02X}, {dflt}, {min}, {max});".format(
            name=self.cname(), addr=self.i2c_address.value, dflt=self.default.value,
            min=self.min.value, max=self.max.value
        )


class Adafruit_MCP4725Plugin(IPlugin, GenericDevicePlugin):

    REQUIRED_SETTINGS = []
    device_class = Adafruit_MCP4725RAAT

    def activate(self):
        pass

    def deactivate(self):
        pass

    def get(self, device):
        i2c_address = device.settings.get(
            "i2c_address", Setting("i2c_address", "", "0x62"))
        i2c_address = i2c_address.parse(lambda s: int(s, 16))

        i2c_address.check(
            lambda v: v in [0x62, 0x63],
            "MCP4725 i2c address should be 0x62 or 0x63 (got 0x{:02X})".format(
                i2c_address.value)
        )

        default = device.settings.get("default", Setting("default", "", "-1"))
        default = default.parse(lambda s: int(s))

        default.check(
            lambda v: v <= 4095 and v >= -1,
            "MCP4725 default should be between 0 and 4095 or -1 for no default (got {})".format(
                default.value)
        )

        min_setting = device.settings.get("min", Setting("min", "", "0"))
        min_setting = min_setting.parse(lambda s: int(s))
        min_setting.check(
            lambda v: v <= 4095 and v >= 0,
            "MCP4725 minimum setting should be between 0 and 4095(got {})".format(
                min_setting.value)
        )

        max_setting = device.settings.get("max", Setting("max", "", "4095"))
        max_setting = max_setting.parse(lambda s: int(s))
        max_setting.check(
            lambda v: v <= 4095 and v >= 0,
            "MCP4725 maximum setting should be between 0 and 4095(got {})".format(
                max_setting.value)
        )

        if max_setting.value < min_setting.value:
            raise Exception("Max setting cannnot be lower than minimum")

        if default.value > max_setting.value:
            raise Exception("Default setting cannnot be higher than maximum")

        if default.value < min_setting.value:
            raise Exception("Default setting cannnot be lower than minimum")

        return Adafruit_MCP4725RAAT(device.name, i2c_address, default, min_setting, max_setting)

    def set_log_level(self, level):
        logging.getLogger(__name__).setLevel(level)
