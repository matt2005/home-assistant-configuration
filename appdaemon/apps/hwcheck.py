import appdaemon.plugins.hass.hassapi as hass

class HWCheck(hass.Hass):

  def initialize(self):
    self.namespace=self.args['namespace']
    self.set_namespace(self.namespace)
    self.listen_event(self.ha_event, "ha_started")
    self.listen_event(self.appd_event, "appd_started")
    
  def ha_event(self, event_name, data, kwargs):
    self.log_notify("Home Assistant is up: {}".format(self.args['namespace']), "INFO")
    self.run_in(self.hw_check, self.args["delay"])
    
  def appd_event(self, event_name, data, kwargs):
    self.log_notify("AppDaemon is up: {}".format(self.args['namespace']), "INFO")
    
  def hw_check(self, kwargs):
    state = self.get_state()
    
    if "zwave" in self.args and self.args["zwave"] not in state:
      self.log_notify("ZWAVE not started after delay period: {}".format(self.args['namespace']), "WARNING")
    if "hue" in self.args and self.args["hue"] not in state:
      self.log_notify("HUE not started after delay period: {}".format(self.args['namespace']), "WARNING")
    if "trafri" in self.args and self.args["tradfri"] not in state:
      self.log_notify("tradfri not running: {}".format(self.args['namespace']), "WARNING")
      
  def log_notify(self, msg, level):
    self.log(msg, level)
    self.notify(msg, name=self.args['notification'])
  
