import logging

from pathlib import Path

from collections import namedtuple

from yapsy.IPlugin import IPlugin

from raat.types import DeviceSource, DeviceInclude

from raat.devices.generic_device import GenericDevice

THIS_PATH = Path(__file__).parent


class TimedOnOff(GenericDevice, namedtuple("TimedOnOff", ["name", "pin", "ontime", "offtime"])):

    __slots__ = ()

    sources = (DeviceSource(THIS_PATH, "timed-onoff.cpp"), )

    includes = (DeviceInclude(THIS_PATH, "timed-onoff.hpp"), )

    @property
    def setup(self):
        return "{name}.setup();".format(name=self.cname())

    @property
    def directory(self):
        return THIS_PATH

    @property
    def declarations(self):
        return "static TimedOnOff {name} = TimedOnOff({pin}, {ontime}, {offtime});".format(
            name=self.cname(), pin=self.pin.value, ontime=self.ontime.value, offtime=self.offtime.value)


class TimedOnOffPlugin(IPlugin):

    device_class = TimedOnOff

    def activate(self):
        pass

    def deactivate(self):
        pass

    def get(self, device):
        return TimedOnOff(device.name, device.settings["pin"], device.settings["ontime"], device.settings["offtime"])

    def set_log_level(self, level):
        logging.getLogger(__name__).setLevel(level)
