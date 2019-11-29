import logging

from pathlib import Path

from collections import namedtuple

from yapsy.IPlugin import IPlugin

from raat.types import DeviceSource, DeviceInclude, LibraryInclude, Setting

from raat.devices.generic_device import GenericDevice, GenericDevicePlugin

THIS_PATH = Path(__file__).parent


class ESP32CaptivePortal(
    GenericDevice,
    namedtuple("ESP32CaptivePortal", ["ap_name", "ap_password", "debug_wifi_manager"])
):

    __slots__ = ()

    sources = (DeviceSource(THIS_PATH, "esp32-captive-portal.cpp"), )

    includes = (
        LibraryInclude("WiFiManager.h"),
        DeviceInclude(THIS_PATH, "esp32-captive-portal.hpp")
    )

    @property
    def required_libraries(self):
        return ["WiFiManager"]

    @property
    def setup(self):
        return "{name}.setup();".format(self.debug_wifi_manager)

    @property
    def command_handler(self):
        return "return {name}.command_handler(command, reply);".format(name=self.cname())

    @property
    def directory(self):
        return THIS_PATH

    @property
    def declarations(self):
        return "static ESP32CaptivePortal {name} = ESP32CaptivePortal();".format()


class ESP32CaptivePortalPlugin(IPlugin, GenericDevicePlugin):

    REQUIRED_SETTINGS = []

    device_class = ESP32CaptivePortal

    def activate(self):
        pass

    def deactivate(self):
        pass

    def get(self, device):

        ap_name = device.settings.get("ap_name",
            Setting("ap_name", "", ""))

        ap_pwd = device.settings.get("ap_pwd",
            Setting("ap_pwd", "", ""))

        debug = device.settings.get("debug",
            Setting("debug", "", "true"))

        return ESP32CaptivePortal(ap_name, ap_pwd, debug)

    def set_log_level(self, level):
        logging.getLogger(__name__).setLevel(level)
