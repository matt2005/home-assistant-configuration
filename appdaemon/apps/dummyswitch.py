import appdaemon.plugins.hass.hassapi as hass

class input_boolean(hass.Hass):

    def initialize(self):
        self.input_boolean = self.args["name"]
        if not self.entity_exists(self.input_boolean):
            self.set_state(self.input_boolean, state = "off")
        self.listen_event(self.change_state, event = "call_service")

    def change_state(self,event_name,data, kwargs):
        if(data["service"] == "turn_off" and data["service_data"]["entity_id"] == self.input_boolean):
            self.log(self.input_boolean + "switched off")
            self.set_state(self.input_boolean, state = "off")
        if(data["service"] == "turn_on" and data["service_data"]["entity_id"] == self.input_boolean):
            self.log(self.input_boolean + "switched on")
            self.set_state(self.input_boolean, state = "on")