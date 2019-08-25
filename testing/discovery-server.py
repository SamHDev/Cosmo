import discovery

server = discovery.DiscoveryServer(port=12892, scheme="_discovery.cosmo.home_device")
server.listen()
