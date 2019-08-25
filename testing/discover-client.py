import discovery


server = discovery.DiscoveryClient(port=12892, scheme="_discovery.cosmo.home_device")
print(server.discovery())