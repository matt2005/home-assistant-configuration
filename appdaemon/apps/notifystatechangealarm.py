import appdaemon.plugins.hass.hassapi as hass
import re


class StateChangeNotify(hass.Hass):
    def initialize(self):
        self.set_namespace(self.args['namespace'])
        self.log_notify("State Change Notifier Ready", "INFO")
        self.listen_state(self.newState, self.args['entity'])

    def newState(self, entity, attribute, old, new, kwargs):
        self.log_notify("{}: {}".format(self.args['message'],
                        self.get_state(self.args['entity'])),
                        "WARNING")

    def log_notify(self, msg, level):
        self.log(msg, level)
        if level == "WARNING":
            self.notify(msg, name=self.args['notification'])
