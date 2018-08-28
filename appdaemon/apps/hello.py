import appdaemon.plugins.hass.hassapi as hass

# Args:
#

class HelloWorld(hass.Hass):

  def initialize(self):
     self.set_namespace("master")
     self.log("Hello from AppDaemon")
     self.log("You are now ready to run Apps!")
