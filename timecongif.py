from onvif import ONVIFCamera
from onvif.exceptions import ONVIFError


camera_ip = "115.242.203.134"  
username = "admin"           
password = "admin@123"        
port = 80                    

def set_time_synchronization():
    try:
        
        camera = ONVIFCamera(camera_ip, port, username, password)
        device_service = camera.create_devicemgmt_service()

        
        time_sync_config = device_service.create_type('SystemDateAndTime')

       
       
        time_sync_config.TimeZone = "UTC"  
        
        
        time_sync_config.NTP = {
            'Enabled': True,  
            'FromDHCP': False,  
            'Manual': {
                'Address': '192.168.1.100',  
                'Port': 123  
            }
        }
        
       
        device_service.SetSystemDateAndTime(time_sync_config)
        
        print("Time synchronization configuration updated successfully!")

    except ONVIFError as e:
        print(f"Error while setting time synchronization: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    set_time_synchronization()
