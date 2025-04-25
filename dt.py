from onvif import ONVIFCamera

# get_system_date_and_time

camera_ip = '115.242.203.134'
port = 80  
username = 'admin1'
password = 'admin@123'

def get_system_date_and_time(camera_ip, username, password, port=80):
    try:
        nvr = ONVIFCamera(camera_ip, port, username, password)
        
        if 'media' in nvr.services:
            media_service = nvr.media
            
        else:
            print("Failed to retrieve system date and time.")
        
       
        system_date_and_time = nvr.devicemgmt.GetSystemDateAndTime()
        print("Date and Time Information:")
        print(f"  Date: {system_date_and_time.UTCDateTime.Date}")
        print(f"  Time: {system_date_and_time.UTCDateTime.Time}")
        print(f"  TimeZone: {system_date_and_time.TimeZone}")
        print(f"  DaylightSavings: {system_date_and_time.DaylightSavings}")
    
    except Exception as e:
        print(f"Error: {e}")

# # Replace with your camera's IP, username, and password
# camera_ip = "192.168.1.100"  # Update with your camera's IP address
# username = "admin"           # Update with your username
# password = "admin"           # Update with your password

# Call the function
get_system_date_and_time(camera_ip, username, password)
