from onvif import ONVIFCamera

def get_users(camera):
    """
    Retrieve the list of users from the ONVIF device.
    """
    try:
        users = camera.devicemgmt.GetUsers()
        print("Users on the device:")
        for user in users:
            print(f"Username: {user.Username}, User Level: {user.UserLevel}")
    except Exception as e:
        print(f"Failed to get users: {e}")

def main():
    
    host = '115.245.98.54'  
    port = 80               
    user = 'admin'          
    password = 'admin@123'   

   
    camera = ONVIFCamera(host, port, user, password)

   
    get_users(camera)

if __name__ == "__main__":
    main()
