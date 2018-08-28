# home-assistant-configuration
Home Assistant configuration files (YAMLs)

This is my Home Assistant Configuration.  
Home Assistant runs on my Raspberry Pi B (256MB), yes it's one of the first ones.

Software on the Pi : HASSbian

**Additional packages installed:**
* ffmpeg
* git

**HASS components and devices:**
* Media_players : 1 OSMC (Kodi), 3 Amazon Firesticks running Kodi, Plex
* Device Trakers: NMAP, owntracks, Bluetooth
* Camera: ONVIF Camera x2
* Speedtest
* Notify: html5, Slack and Kodi
* Switch: WOL
* MQTT Switches and sensors via RFlink to Mqtt using a ESP NodeMCU.
* pihole sensors, and switch to disable pihole
* MetOffice weather sensors
* Google GeoCode custom component [link](https://github.com/michaelmcarthur/GoogleGeocode-HASS)
* Various System monitors
* Floorplan, currently only setup using default plan.
* CustomUI
* Heating logic, via AppDaemon (in testing)
* Workday sensor
* Ikea Tradfri (currently disabled due to firmware issue)
* Battery Alerts [link](https://community.home-assistant.io/t/howto-create-battery-alert-without-creating-a-template-for-every-device/30576)

Notifies via slack channel when HASS updates are available

Screenshots
![Screenshot 1](/images/hass1.png)
![Screenshot 2](/images/hass2.png)

The setup this I've written a script
>wget -Nnv https://gist.githubusercontent.com/matt2005/32011478f1c3bf54f58ca57042702517/raw/homeassistant_setup.sh && chown pi:pi homeassistant_setup.sh && bash homeassistant_setup.sh

  
To update
>wget -Nnv https://gist.githubusercontent.com/matt2005/21f1204cea47d437001070689c90bb85/raw/update_homeassistant.sh && chown pi:pi update_homeassistant.sh && bash update_homeassistant.sh
