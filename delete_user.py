from onvif import ONVIFCamera

def delete_user(host, port, username, password, delete_username):
    """
    Deletes a user from an ONVIF-compliant device.

    :param host: The IP address of the ONVIF device.
    :param port: The port number of the ONVIF device (default is typically 80).
    :param username: The admin username for the ONVIF device.
    :param password: The admin password for the ONVIF device.
    :param delete_username: The username of the account to be deleted.
    """
    try:
        # Connect to the ONVIF device
        camera = ONVIFCamera(host, port, username, password)

        # Delete the specified user
        print(f"Deleting user '{delete_username}'...")
        camera.devicemgmt.DeleteUsers([delete_username])
        print(f"User '{delete_username}' has been successfully deleted.")
    except Exception as e:
        print(f"An error occurred while deleting the user: {e}")


delete_user(
    host="192.168.1.2",       
    port=80,                  
    username="admin",         
    password="adminpassword", 
    delete_username="user1"   
)
