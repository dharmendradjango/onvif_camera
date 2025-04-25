from onvif import ONVIFCamera


def connect_to_onvif(ip, port, username, password):
    try:
        
        camera = ONVIFCamera(ip, port, username, password)
        return camera
    except Exception as e:
        print(f"Error connecting to ONVIF device: {e}")
        return None


def get_device_info(camera):
    try:
        device_info = camera.devicemgmt.GetDeviceInformation()
        return device_info
    except Exception as e:
        print(f"Error retrieving device information: {e}")
        return None


if __name__ == "__main__":
    
    device_ip = "115.242.203.134"  
    device_port = 80             
    username = "admin"           
    password = "admin@123"        

    
    camera = connect_to_onvif(device_ip, device_port, username, password)

    if camera:
        
        device_info = get_device_info(camera)
        if device_info:
            print(f"Device Model: {device_info.Model}")
            print(f"Firmware Version: {device_info.FirmwareVersion}")
            print(f"Serial Number: {device_info.SerialNumber}")
            print(f"Hardware ID: {device_info.HardwareId}")
    else:
        print("Failed to connect to the ONVIF device.")
