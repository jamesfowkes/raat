class GenericDevice:

	def cname(self, static=True):
		sanitised_name = self.name.lower().replace(" ", "_")
		if static:
			return "s_" + sanitised_name
		else:
			return sanitised_name

	@property
	def command_handler(self):
		return "return {name}.command_handler(command, reply);".format(name=self.cname())

class GenericDevicePlugin:

	def verify_settings(self, device):

		for setting in self.REQUIRED_SETTINGS:
			if setting not in device.settings:
				raise Exception("Expected setting {} in device '{}'".format(setting, device.name))