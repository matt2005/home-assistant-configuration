import appdaemon.plugins.hass.hassapi as hass
import datetime

# Declare Class
class TestSensors(hass.Hass):
  #initialize() function which will be called at startup and reload
  def initialize(self):
    self.namespace=self.args['namespace']
    self.set_namespace(self.namespace)
    # Call to Home Assistant to turn the porch light on
    self.log("Setting flow temp ...")
    self.set_state("sensor.heating_flow_temp", state = 20, attributes={"unit_of_measurement": "°C", "friendly_name": "FlowTemp","icon": "mdi:oil-temperature"})
    self.log("Setting outside temp ...")
    self.set_state("sensor.heating_outside_temp", state = 10, attributes={"unit_of_measurement": "°C", "friendly_name": "OutsideTemp"})
    self.log("Setting set point ...")
    self.set_state("input_slider.heating_setpoint_temp", state = 20, attributes={"initial": 0, "min": 0, "max": 35, "step": 1, "friendly_name": "SetPoint","icon": "mdi:thermometer-lines"})
    self.log("Setting switch heating ...")
    self.set_state("switch.heating", state = "off", attributes={"assumed_state": False, "friendly_name": "Switch","icon": "mdi:radiator"})
    self.log("Setting group ...")
    self.set_state("group.heating", state = "off", attributes={"assumed_state": False, "friendly_name": "HeatingLogicTest", "entity_id": ["sensor.heating_flow_temp","sensor.heating_outside_temp","input_slider.heating_setpoint_temp","switch.heating"]})
    
    
