from onvif import ONVIFCamera, ONVIFError

# nvr_ip = '115.242.203.134'
# nvr_port = 80  
# username = 'admin'
# password = 'admin@123'

# nvr_ip = '115.245.98.54'
nvr_ip = '14.195.152.243'
nvr_port = 80 
username = 'admin'
password = 'admin@123'

# camera_ip = '115.242.156.166'
# port = 5555  
# username = 'admin'
# password = 'oasis@123'

try:
    nvr = ONVIFCamera(nvr_ip, nvr_port, username, password)

    # Check if media service is available
    if 'media' in nvr.services:
        media_service = nvr.media
    else:
        print("Media service is not available.")


    # Get device information
    device_info = nvr.devicemgmt.GetDeviceInformation()
    print("Device Information:")
    print(f"Manufacturer: {device_info.Manufacturer}")
    print(f"Model: {device_info.Model}")
    print(f"Firmware Version: {device_info.FirmwareVersion}")
    print(f"Serial Number: {device_info.SerialNumber}")
    print(f"Hardware ID: {device_info.HardwareId}")
   
    




 
    try:
        log_type = {'Type': 'Event'}  # Modify as needed
        logs = nvr.devicemgmt.GetSystemLog('Event')
        print(str(logs))
        print("\nSystem Logs:")
        for log in logs:
            print(str(log))
    except ONVIFError as log_err:
        print(f"Error retrieving system logs: {log_err}")
except ONVIFError as err:
    print(f"Error: {err}")



