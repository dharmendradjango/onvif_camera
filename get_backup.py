from onvif import ONVIFCamera
import base64
import os

# GetSystemBackupRequest 
camera_ip = "115.242.203.134"  
username = "admin"           
password = "admin@123"        
port = 80        

def backup_configuration():
    try:
        
        print("Connecting to the ONVIF device...")
        camera = ONVIFCamera(camera_ip, port, username, password)

        if 'media' in camera.services:
            device_service = camera.media
        else:
            print("Media service is not available.")
        device_service = camera.create_devicemgmt_service()

        
        print("Requesting system backup files...")
        backup_files = device_service.GetSystemBackup()

        # Step 3: Process the returned backup files
        for index, backup_file in enumerate(backup_files):
            name = backup_file.Name or f"backup_{index + 1}"
            mime_type = backup_file.MimeType
            data = backup_file.Data

            # Decode the binary data
            decoded_data = base64.b64decode(data)

            # Save the backup file locally
            file_extension = mime_type.split('/')[-1]  # Guess the file extension
            filename = f"{name}.{file_extension}"
            with open(filename, "wb") as file:
                file.write(decoded_data)
                print(f"Backup file saved: {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
backup_configuration()
