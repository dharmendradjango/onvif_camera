from onvif import ONVIFCamera

# Device connection details
camera_ip = '115.242.203.134'
port = 80  
username = 'admin'
password = 'admin@123'       


def connect_with_ws_usernametoken():
    try:
       
        camera = ONVIFCamera(camera_ip, port, username, password)
        
        
        # Example: Get device information
        device_service = camera.create_devicemgmt_service()
        device_info = device_service.GetDeviceInformation()
        print("Device Information:", device_info)
    except Exception as e:
        print(f"An error occurred: {e}")

connect_with_ws_usernametoken()
