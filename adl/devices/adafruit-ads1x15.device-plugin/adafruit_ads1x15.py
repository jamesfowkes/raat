import logging
import os

from pathlib import Path

from collections import namedtuple

from yapsy.IPlugin import IPlugin

from adl.types import DeviceSource, DeviceInclude

from adl.devices.generic_device import GenericDevice, GenericDevicePlugin
from adl.types import Setting

THIS_PATH = Path(__file__).parent

class Adafruit_ADS1x15(GenericDevice, namedtuple("Adafruit_ADS1x15", ["name", "ads_type", "multiplier"])):

	__slots__ = ()

	@property
	def setup(self):
		return "{name}.setup();".format(name=self.cname())

	@property
	def directory(self):
		return THIS_PATH

	@property
	def sources(self):
		return [DeviceSource(THIS_PATH, "adafruit-ads1x15.cpp")]

	@property
	def includes(self):
		return [
			LocalInclude("adafruit-ads1x15.h"),
			LibraryInclude("Adafruit_ADS1015.h")
		]

	@property
	def declarations(self):
		return "static Adafruit_ADS1x15 {name} = Adafruit_ADS1x15({ads_type}, {multiplier});".format(
			name=self.cname(), ads_type=self.ads_type.value, multiplier=self.multiplier.value)

class Adafruit_ADS1x15Plugin(IPlugin, GenericDevicePlugin):

	REQUIRED_SETTINGS = ["ads_type"]

	def activate(self):
		pass

	def deactivate(self):
		pass

	def get(self, device):
		self.verify_settings(device)
		multiplier = device.settings.get("multiplier", Setting("multiplier", "", 1.0))

		if device.settings["ads_type"].value == "ADS1015":
			ads_type = Setting("ads_type", "ads_type", "ADC_SUBTYPE_ADS1015")
		elif device.settings["ads_type"].value == "ADS1115":
			ads_type = Setting("ads_type", "ads_type", "ADC_SUBTYPE_ADS1115")
		else:
			raise Exception("ads_type must be one of ADS1015, ADS1115 (got {})".format(device.settings["ads_type"]))

		return Adafruit_ADS1x15(device.name, ads_type, multiplier)

	def set_log_level(self, level):
		logging.getLogger(__name__).setLevel(level)
