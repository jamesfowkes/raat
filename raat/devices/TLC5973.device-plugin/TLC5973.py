import logging

from pathlib import Path

from collections import namedtuple

from yapsy.IPlugin import IPlugin

from raat.types import DeviceSource, DeviceInclude

from raat.devices.generic_device import GenericDevice

THIS_PATH = Path(__file__).parent


class TLC5973(GenericDevice, namedtuple("TLC5973", ["name", "num_leds", "pin"])):

    __slots__ = ()

    sources = (DeviceSource(THIS_PATH, "TLC5973.cpp"), )

    includes = (DeviceInclude(THIS_PATH, "TLC5973.hpp"), )

    @property
    def setup(self):
        return "{name}.setup();".format(name=self.cname())

    @property
    def directory(self):
        return THIS_PATH

    @property
    def declarations(self):
        return "static TLC5973 {name} = TLC5973({num_leds}, {pin});".format(
            name=self.cname(), num_leds=self.num_leds.value, pin=self.pin.value)


class TLC5973Plugin(IPlugin):

    device_class = TLC5973

    def activate(self):
        pass

    def deactivate(self):
        pass

    def get(self, device):
        return TLC5973(device.name, device.settings["num_leds"], device.settings["pin"])

    def set_log_level(self, level):
        logging.getLogger(__name__).setLevel(level)
