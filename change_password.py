from onvif import ONVIFCamera

def change_user_password(device_address, username, password, port, user_to_change, new_password):
    try:
        
        camera = ONVIFCamera(device_address, port, username, password)
        device_service = camera.create_devicemgmt_service()

        
        users = device_service.GetUsers()

        
        for user in users:
            if user.Username == user_to_change:
                
                user.Password = new_password
                
                
                
                device_service.SetUser([user])
                print(f"Password for user '{user_to_change}' changed successfully.")
                return

        print(f"User '{user_to_change}' not found.")

    except Exception as e:
        print(f"An error occurred: {e}")


DEVICE_ADDRESS = "192.168.1.100"  
USERNAME = "admin"               
PASSWORD = "admin_password"      
PORT = 80                        
USER_TO_CHANGE = "username"      
NEW_PASSWORD = "newpassword"     

# Change the user's password
change_user_password(DEVICE_ADDRESS, USERNAME, PASSWORD, PORT, USER_TO_CHANGE, NEW_PASSWORD)
