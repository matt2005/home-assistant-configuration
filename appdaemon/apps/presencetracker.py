import appdaemon.plugins.hass.hassapi as hass


class PresenceTracker(hass.Hass):

    def initialize(self):
        self.set_namespace(self.args['namespace'])
        self.log_notify("Presence Tracker Ready", "INFO")
        # Set Initial State
        self.set_devicetracker_state(self.args["binary_sensor"])
        # Subscribe to sensors
        self.listen_state(self.state_change_detected,
                          self.args["binary_sensor"])

    def set_devicetracker_state(self, entity):
        currentstate = self.get_state(self.args["binary_sensor"])
        if currentstate == "on":
            # Person is home so set device tracker to home
            self.log_notify("setting home", "INFO")
            self.set_state(self.args["device_tracker"], state="home",
                           attributes={"friendly_name":
                                       self.args["friendly_name"]})
        elif currentstate == "off":
            # Person is not home so set device tracker to away
            self.log_notify("setting not_home", "INFO")
            self.set_state(self.args["device_tracker"], state="not_home",
                           attributes={"friendly_name":
                                       self.args["friendly_name"]})

    def state_change_detected(self, entity, attribute, old,
                              new, kwargs):
        device_name = self.split_entity(self.args['device_tracker'])[1]
        if not (self.check_group(self.args['device_tracker'],
                self.args['known_devices'])):
            self.log_notify("Adding device to trusted: {}"
                            .format(device_name), "WARNING")
            self.set_group(self.args['device_tracker'],
                           self.args['known_devices'])
        self.set_devicetracker_state(entity)

    def set_group(self, entity, group):
        groupcheck = self.get_state(group, attribute="all")
        if groupcheck["attributes"]["entity_id"] is None:
            self.log_notify("Adding group: {}"
                            .format(entity.lower()), "WARNING")
            self.set_state(group, state="off",
                           attributes={"assumed_state": False,
                                       "friendly_name": "KnownDevices",
                                       "entity_id": [entity.lower()]})
        else:
            membership = groupcheck["attributes"]["entity_id"].append(
                entity.lower())
            self.log_notify("updating group membership: {}"
                            .format(entity.lower()), "INFO")
            self.set_state(entity,
                           attributes={"assumed_state": False,
                                       "entity_id": [membership]})

    def check_group(self, entity, group):
        groupcheck = self.get_state(group, attribute="all")
        if groupcheck["attributes"]["entity_id"] is not None:
            return entity in groupcheck["attributes"]["entity_id"]
        else:
            return False

    def log_notify(self, msg, level):
        self.log(msg, level)
        if level == "WARNING":
            self.notify(msg, name=self.args['notification'])
