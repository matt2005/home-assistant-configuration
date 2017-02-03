#!/bin/bash
adb kill-server
adb start-server
adb connect $1
adb shell am start -n org.xbmc.kodi/.Splash
adb disconnect
adb kill-server