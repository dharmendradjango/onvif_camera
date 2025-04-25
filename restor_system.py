from onvif import ONVIFCamera
import base64
import os


camera_ip = "115.242.203.134"  
username = "admin"           
password = "admin@123"        
port = 80       

def read_backup_file(file_path):
    """
    Reads a backup file from disk and returns its Base64-encoded content and file name.
    :param file_path: Path to the backup file (string)
    :return: Dictionary containing file name and Base64-encoded data
    """
    try:
        with open(file_path, "rb") as file:
            binary_data = file.read()
        return {
            "Name": os.path.basename(file_path),
            "Data": base64.b64encode(binary_data).decode('utf-8')
        }
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def restore_system_configuration(file_list):
    """
    Restores system configuration files to an ONVIF device.
    :param file_list: List of file paths to be restored (list of strings)
    """
    try:
        # Step 1: Read and prepare backup files
        backup_files = []
        for file_path in file_list:
            print(f"Processing file: {file_path}")
            backup_file = read_backup_file(file_path)
            if backup_file:
                backup_files.append(backup_file)

        if not backup_files:
            print("No valid backup files to restore.")
            return

        
        camera = ONVIFCamera(camera_ip, port, username, password)
        device_service = camera.create_devicemgmt_service()

       
        device_service.RestoreSystem(backup_files)
        print("System configuration restored successfully.")

    except Exception as e:
        print(f"An error occurred during the restore process: {e}")

# File paths to be restored
backup_file_list = [
    "system_settings.zip",  # Replace with actual file path
    "user_settings.zip"     # Replace with actual file path
]

# Run the program
restore_system_configuration(backup_file_list)
