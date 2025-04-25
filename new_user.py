from onvif import ONVIFCamera

def register_user(host, port, username, password, new_username, new_password, user_level="Administrator"):
    """
    Registers a new user to an ONVIF-compliant device.

    :param host: The IP address of the ONVIF device.
    :param port: The port number of the ONVIF device (default is typically 80).
    :param username: The current admin username for the ONVIF device.
    :param password: The current admin password for the ONVIF device.
    :param new_username: The username for the new user.
    :param new_password: The password for the new user.
    :param user_level: The user level for the new user. Default is "Administrator".
    """
    try:
        
        camera = ONVIFCamera(host, port, username, password)

        # Create user information for registration
        user_info = {
            "Username": new_username,
            "Password": new_password,
            "UserLevel": user_level,
        }

        # Register the new user
        print(f"Registering user '{new_username}' with user level '{user_level}'...")
        camera.devicemgmt.CreateUsers([user_info])
        print(f"User '{new_username}' has been successfully registered.")
    except Exception as e:
        print(f"An error occurred while registering the user: {e}")

# Replace with your device's details
register_user(
    host="115.242.203.134",       
    port=80,                 
    username="admin",         
    password="admin@123", 
    new_username="admin1",   
    new_password="admin@123", 
    user_level="Administrator"  
)
