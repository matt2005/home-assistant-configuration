import appdaemon.plugins.hass.hassapi as hass
import re


class DeviceNotify(hass.Hass):
    def initialize(self):
        self.set_namespace(self.args['namespace'])
        self.log_notify("Device Notifier Ready", "INFO")
        self.listen_state(self.newDevice, "device_tracker", new="home")

    def newDevice(self, entity, attribute, old, new, kwargs):
        device_name = self.split_entity(entity)[1]
        if (self.check_group(entity, self.args['known_devices'])):
            self.log_notify("Trusted device connected: {}"
                            .format(device_name), "INFO")
        else:
            self.log_notify("Untrusted device connected: {}"
                            .format(device_name), "WARNING")

    def log_notify(self, msg, level):
        self.log(msg, level)
        if level == "WARNING":
            self.notify(msg, name=self.args['notification'])

    def check_group(self, entity, group):
        group = self.get_state(group, attribute="all")
        return entity in group["attributes"]["entity_id"]
