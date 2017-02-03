# home-assistant-configuration
Home Assistant configuration files (YAMLs)

This is my Home Assistant Configuration.  
Home Assistant runs on my Raspberry Pi B (256MB), yes it's one of the first ones.

Software on the Pi : HASSbian

** Additional packages installed: **
* avconv
* git

** HASS components and devices **
* Media_players :1 OSMC (Kodi), 3 Amazon Firesticks runnong Kodi
* Device Trakers: NMAP, owntracks
* Camera:ffmpeg  to a sricam ipcam (Currently Disabled)
* Speedtest

Notifies via slack channel when HASS updates are available

The setup this I've written a script
>wget -Nnv https://gist.githubusercontent.com/matt2005/32011478f1c3bf54f58ca57042702517/raw/homeassistant_setup.sh && chown pi:pi homeassistant_setup.sh && bash homeassistant_setup.sh

  
To update
>wget -Nnv https://gist.githubusercontent.com/matt2005/21f1204cea47d437001070689c90bb85/raw/update_homeassistant.sh && chown pi:pi update_homeassistant.sh && bash update_homeassistant.sh
