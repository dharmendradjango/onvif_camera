from onvif import ONVIFCamera

def change_user_password(host, port, username, password, target_username, new_password, user_level="Administrator"):
    """
    Changes the password for an existing user on an ONVIF-compliant device.

    :param host: The IP address of the ONVIF device.
    :param port: The port number of the ONVIF device (default is typically 80).
    :param username: The current admin username for the ONVIF device.
    :param password: The current admin password for the ONVIF device.
    :param target_username: The username whose password is to be changed.
    :param new_password: The new password for the user.
    :param user_level: The authority level for the user. Default is "Administrator".
    """
    try:
        # Connect to the ONVIF device
        camera = ONVIFCamera(host, port, username, password)

        # Create the user info to update
        user_info = {
            "Username": target_username,
            "Password": new_password,
            "UserLevel": user_level,
        }

        # Update the user information
        print(f"Changing password for user '{target_username}'...")
        camera.devicemgmt.SetUser([user_info])
        print(f"Password for user '{target_username}' has been successfully updated.")
    except Exception as e:
        print(f"An error occurred while changing the user password: {e}")


change_user_password(
    host="192.168.1.2",        
    port=80,                   
    username="admin",          
    password="adminpassword", 
    target_username="user1",   
    new_password="newpassword", 
    user_level="Administrator"  
)
