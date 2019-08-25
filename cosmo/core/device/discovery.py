from . import discoveryapi as discovery

PORT = 12892
SCHEME = "_discovery.cosmo.home_device"


class CosmoDeviceDiscovery:
    def __init__(self, device):
        self.device = device
        self.client = discovery.DiscoveryServer(port=PORT, scheme=SCHEME)

        @self.client.discovery_callback
        def on_msg(cls: discovery.DiscoveryRequestMessage):
            data = {}
            data["name"] = self.device.name
            if data["name"] is None:
                data["name"] = self.device.hotspot.ssid
            data["setup"] = self.device.is_setup
            cls.reply(data=data)

    def listen(self):
        self.device.cosmo.logger.debug(f"Starting Network Discovery Server on port '{PORT}' with scheme '{SCHEME}'")
        self.client.listen(True)
