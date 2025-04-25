from onvif import ONVIFCamera


camera_ip = "115.242.203.134"  
username = "admin"           
password = "admin@123"        
port = 80                    

def print_ip_address(address, prefix_length):
    print(f"IP Address: {address}, Prefix Length: {prefix_length}")

def main():
    
    my_camera = ONVIFCamera(camera_ip, port, username, password)
    device_service = my_camera.create_devicemgmt_service()

    
    network_interface_list = device_service.GetNetworkInterfaces()

    eth0 = None
    for network_interface in network_interface_list:
        if (
            hasattr(network_interface, "Info") and
            hasattr(network_interface.Info, "Name") and
            network_interface.Info.Name == "eth0"
        ):
            eth0 = network_interface
            break

    # Step 3: Show the IPv4 configuration for "eth0"
    if eth0 and hasattr(eth0, "IPv4"):
        ipv4_config = eth0.IPv4.Config

        if hasattr(ipv4_config, "Manual"):
            for manual in ipv4_config.Manual:
                print_ip_address(manual.Address, manual.PrefixLength)

        if hasattr(ipv4_config, "LinkLocal"):
            link_local = ipv4_config.LinkLocal
            print_ip_address(link_local.Address, link_local.PrefixLength)

        if hasattr(ipv4_config, "FromDHCP"):
            dhcp = ipv4_config.FromDHCP
            print_ip_address(dhcp.Address, dhcp.PrefixLength)

        if hasattr(ipv4_config, "DHCP"):
            print(f"DHCP Enabled: {ipv4_config.DHCP}")
    else:
        print("No IPv4 configuration found for eth0")

if __name__ == "__main__":
    main()
