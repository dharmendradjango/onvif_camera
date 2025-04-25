from onvif import ONVIFCamera

# network configurations
# camera_ip = '115.242.156.166'
# port = 5555  
# username = 'admin'
# password = 'oasis@123'

camera_ip = '192.168.0.65'
port = 80
username = 'admin'
password = 'admin123'


camera = ONVIFCamera('115.245.98.54', 80, 'admin', 'admin@123')


devicemgmt = camera.create_devicemgmt_service()


interfaces = devicemgmt.GetNetworkInterfaces()


for interface in interfaces:
    print(f"Name: {interface.Info.Name}")
    print(f"Enabled: {interface.Enabled}")
    print(f"MAC Address: {interface.Info.HwAddress}")
    if interface.IPv4:
        print(f"IPv4 Address: {interface.IPv4.Config.Manual[0].Address}")
        print(f"DHCP: {interface.IPv4.Config.DHCP}")
