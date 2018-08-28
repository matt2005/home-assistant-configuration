import appdaemon.plugins.hass.hassapi as hass

class HeatingLogic(hass.Hass):

    def initialize(self):
        self.set_namespace(self.args['namespace'])
        self.log("Starting HeatingLogic ...")
        self.gain = float(self.args['gain'])
        self.adjustment = float(self.args['adjustment'])
        self.temperature_flow_min = float(self.args['temperature_flow_min'])
        self.temperature_flow_max = float(self.args['temperature_flow_max'])
        self.temperature_flow_tolerance_above = float(self.args['temperature_flow_tolerance_above'])
        self.temperature_flow_tolerance_below = float(self.args['temperature_flow_tolerance_below'])
        self.switch_heating = self.args['switch_heating']
        self.switch_heating_max_on = float(self.args['switch_heating_max_on'])    # Minutes

        # Get current temperature information
        self.get_sensor_temperatures()
        
        # Register for sensor status updates
        self.listen_state(self.temperature_change, entity=self.args['sensor_temperature_outside_actual'])
        self.listen_state(self.temperature_change, entity=self.args['sensor_temperature_flow_actual'])
        self.listen_state(self.temperature_change, entity=self.args['input_temperature_inside_setpoint'])

        # Set inital power state 
        self.action_heating()

    def get_sensor_temperatures(self, update_entity="", update_value=0.0):
        # Get values from HA
        if not update_entity:
            self.temperature_outside_actual = float(self.get_state(self.args['sensor_temperature_outside_actual']))
            self.temperature_flow_actual = float(self.get_state(self.args['sensor_temperature_flow_actual']))
            self.temperature_inside_setpoint = float(self.get_state(self.args['input_temperature_inside_setpoint']))
        elif update_entity == self.args['sensor_temperature_outside_actual']:
            self.temperature_outside_actual = update_value
        elif update_entity == self.args['sensor_temperature_flow_actual']:
            self.temperature_flow_actual = update_value
        elif update_entity == self.args['input_temperature_inside_setpoint']:
            self.temperature_inside_setpoint = update_value

    def calculate_temperature_flow_setpoint(self):
        """
            Calculate best vorlauftemperatur
        """
        temperature_flow_setpoint = float(min(max(0.55*self.gain*(self.temperature_inside_setpoint**(self.temperature_outside_actual/(320-self.temperature_outside_actual*4)))*((-self.temperature_outside_actual+20)*2)+self.temperature_inside_setpoint+self.adjustment, self.temperature_flow_min), self.temperature_flow_max))
        return temperature_flow_setpoint

    def calculate_heating_action(self):
        """
            Decide wether to turn heating on, off or to leave it in its current state
        """
        temperature_flow_setpoint = self.calculate_temperature_flow_setpoint()
        self.log("T-flow-setpoint: "+str(temperature_flow_setpoint) +" => ")
        if self.temperature_flow_actual < (temperature_flow_setpoint-self.temperature_flow_tolerance_below):
            return "on"
        elif self.temperature_flow_actual >= (temperature_flow_setpoint+self.temperature_flow_tolerance_above): 
            return "off"
        else:
            return ""
    
    def temperature_change(self, entity, attribute, old, new, kwargs):
        """
            Callback function
            called if any temperature changes
        """
        self.get_sensor_temperatures(update_entity=entity, update_value=float(new))
        self.action_heating()

    def action_heating(self):
        """
            Action: Turn heating on or off
        """

        # Decide to turn heating on or off
        calculated_action = self.calculate_heating_action()
        
        # Execute action
        if calculated_action == "on":
            self.action_heating_on({})
        elif calculated_action == "off":
            self.action_heating_off({})
        else:
            self.log("Leaving heating in its current state (T-flow-actual: %f; T-outside-actual: %f; T-inside-setpoint: %f)" % (self.temperature_flow_actual, self.temperature_outside_actual, self.temperature_inside_setpoint))

    def action_heating_on(self, kwargs):
        self.log("Turning heating on (T-flow-actual: %f; T-outside-actual: %f; T-inside-setpoint: %f)" % (self.temperature_flow_actual, self.temperature_outside_actual, self.temperature_inside_setpoint))
        self.call_service("switch/turn_on", entity_id=self.switch_heating)
            
        # Set timer for auto turn off to prevent damage
        self.turn_off_timer = self.run_in(self.action_heating_off, int(60*self.switch_heating_max_on), timer=True)

    def action_heating_off(self, kwargs):
        if 'timer' in kwargs and kwargs['timer']==True:
            self.log("Timeout reached for heating in state 'on'. Going to turn it off =>")
        self.log("Turning heating off (T-flow-actual: %f; T-outside-actual: %f; T-inside-setpoint: %f)" % (self.temperature_flow_actual, self.temperature_outside_actual, self.temperature_inside_setpoint))
        self.call_service("switch/turn_off", entity_id=self.switch_heating)

        # cancel timer for auto turn off
        if hasattr(self, 'turn_off_timer'):
            self.cancel_timer(self.turn_off_timer)
            self.log("Canceled turn_off timer")
