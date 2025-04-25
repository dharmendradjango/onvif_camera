from onvif import ONVIFCamera


camera_ip = "115.242.203.134"  
username = "admin"           
password = "admin@123"        
port = 80   

def configure_time_synchronization():
    try:
        
        mycam = ONVIFCamera(camera_ip, port, username, password)
        device_service = mycam.create_devicemgmt_service()

       
        system_date_and_time = device_service.GetSystemDateAndTime()
        print("Current System Date and Time Settings:")
        print(system_date_and_time)

        
        if system_date_and_time.DateTimeType != "NTP":
            print("NTP is not in use. Configuring NTP using DHCP...")

            
            from_dhcp = True
            ntp_manual = []  

            
            device_service.SetNTP(NTPFromDHCP=from_dhcp, NTPManual=ntp_manual)
            print("NTP configuration updated to use DHCP.")

            
            device_service.SetSystemDateAndTime(
                DateTimeType="NTP",
                DaylightSavings=system_date_and_time.DaylightSavings,
                TimeZone=system_date_and_time.TimeZone,
            )
            print("System time synchronization with NTP enabled.")
        else:
            print("NTP is already in use.")

    except Exception as e:
        print("An error occurred:", e)


configure_time_synchronization()
