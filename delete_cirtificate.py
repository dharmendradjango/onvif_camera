from onvif import ONVIFCamera

# Define device credentials and connection details
device_ip = "192.168.1.100"  # Replace with the IP address of your device
device_port = 80             # Port number (default is 80)
username = "admin"           # Username for the device
password = "password"        # Password for the device

# Initialize the ONVIF camera client
client = ONVIFCamera(device_ip, device_port, username, password)

# Access the device management service
devicemgmt_service = client.create_devicemgmt_service()

# Certificate IDs to delete (example)
certificate_ids = ["cert1", "cert2"]  # Replace with actual CertificateIDs

# Delete certificates
for cert_id in certificate_ids:
    try:
        devicemgmt_service.DeleteCertificates(CertificateID=[cert_id])
        print(f"Certificate {cert_id} successfully deleted.")
    except Exception as e:
        print(f"Failed to delete certificate {cert_id}: {e}")
