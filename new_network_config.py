from onvif import ONVIFCamera


camera_ip = "115.242.203.134"  
username = "admin"         
password = "admin@123"      
port = 80                  


new_ip_address = "115.242.203.135"
new_prefix_length = 24     
dhcp_enabled = False       

try:
    
    camera = ONVIFCamera(camera_ip, port, username, password)

    
    dev_mgmt_service = camera.create_devicemgmt_service()

    
    network_interfaces = dev_mgmt_service.GetNetworkInterfaces()

    
    for iface in network_interfaces:
        if iface.Token == "eth0":  
            
            config = iface
            config.Enabled = True
            config.IPv4.Enabled = True
            config.IPv4.DHCP = dhcp_enabled
            config.IPv4.Manual = [{"Address": new_ip_address, "PrefixLength": new_prefix_length}]

            
            reboot_needed = dev_mgmt_service.SetNetworkInterfaces(
                {"InterfaceToken": iface.Token, "NetworkInterface": config}
            )

           
            if reboot_needed:
                print("Rebooting device to apply new settings...")
                dev_mgmt_service.SystemReboot()
                print("Device rebooted successfully.")

            print(f"Network interface {iface.Token} updated to {new_ip_address}")
            break
    else:
        print("Interface 'eth0' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
