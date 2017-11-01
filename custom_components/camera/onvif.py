"""
Support for ONVIF Cameras with FFmpeg as decoder.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/camera.onvif/
"""
import asyncio
import logging
import os

import voluptuous as vol

from homeassistant.const import (
    CONF_NAME, CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_PORT)
from homeassistant.components.camera import Camera, PLATFORM_SCHEMA
from homeassistant.components.ffmpeg import (
    DATA_FFMPEG)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import (
    async_aiohttp_proxy_stream)

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['onvif-zeep==0.2.7']
DEPENDENCIES = ['ffmpeg']
DEFAULT_NAME = 'ONVIF Camera'
DEFAULT_PORT = 5000
DEFAULT_USERNAME = 'admin'
DEFAULT_PASSWORD = '888888'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_PASSWORD, default=DEFAULT_PASSWORD): cv.string,
    vol.Optional(CONF_USERNAME, default=DEFAULT_USERNAME): cv.string,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
})


@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up a ONVIF camera."""
    if not hass.data[DATA_FFMPEG].async_run_test(config.get(CONF_HOST)):
        return
    async_add_devices([ONVIFCamera(hass, config)])


class ONVIFCamera(Camera):
    """An implementation of an ONVIF camera."""

    def __init__(self, hass, config):
        """Initialize a ONVIF camera."""
        from onvif import ONVIFCamera
        import onvif
        super().__init__()

        self._name = config.get(CONF_NAME)
        self._ffmpeg_arguments = '-q:v 2'
        try:
            mycam = ONVIFCamera(
                config.get(CONF_HOST), config.get(CONF_PORT),
                config.get(CONF_USERNAME), config.get(CONF_PASSWORD)
            )
            media_service = mycam.create_media_service()
            profiles = media_service.GetProfiles()
            token = profiles[0].token
            stream_uri = media_service.GetStreamUri(
                {'StreamSetup': {
                    'Stream': 'RTP-Unicast', 'Transport': 'UDP'
                    }, 'ProfileToken': token}
                )
        except Exception as err:
            _LOGGER.error("Unable to communicate with ONVIF Camera: %s", err)

        self._input = stream_uri.Uri.replace(
            'rtsp://', 'rtsp://{}:{}@'.format(config.get(
              CONF_USERNAME), config.get(CONF_PASSWORD)), 1)
        _LOGGER.debug("ONVIF Camera Using the following URL for %s: %s",
                      self._name, self._input)

    @asyncio.coroutine
    def async_camera_image(self):
        """Return a still image response from the camera."""
        from haffmpeg import ImageFrame, IMAGE_JPEG
        ffmpeg = ImageFrame(
            self.hass.data[DATA_FFMPEG].binary, loop=self.hass.loop)

        image = yield from asyncio.shield(ffmpeg.get_image(
            self._input, output_format=IMAGE_JPEG,
            extra_cmd=self._ffmpeg_arguments), loop=self.hass.loop)
        return image

    @asyncio.coroutine
    def handle_async_mjpeg_stream(self, request):
        """Generate an HTTP MJPEG stream from the camera."""
        from haffmpeg import CameraMjpeg

        stream = CameraMjpeg(self.hass.data[DATA_FFMPEG].binary,
                             loop=self.hass.loop)
        yield from stream.open_camera(
            self._input, extra_cmd=self._ffmpeg_arguments)

        yield from async_aiohttp_proxy_stream(
            self.hass, request, stream,
            'multipart/x-mixed-replace;boundary=ffserver')
        yield from stream.close()

    @property
    def name(self):
        """Return the name of this camera."""
        return self._name
