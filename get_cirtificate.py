from onvif import ONVIFCamera

# Replace with your device details
camera_ip = '115.242.203.134'
port = 80  
username = 'admin'
password = 'admin@123'           

# Create an ONVIF camera object
camera = ONVIFCamera(camera_ip, port, username, password)

# Access the device management service
device_service = camera.create_devicemgmt_service()

# Get the certificate statuses
certificate_statuses = device_service.GetCertificatesStatus()

if certificate_statuses:
    # Get the CertificateID of the first certificate
    first_certificate_id = certificate_statuses[0].CertificateID

    # Retrieve detailed certificate information
    certificate_info = device_service.GetCertificateInformation(CertificateID=first_certificate_id)
    
    # Display the certificate information
    print("Certificate Information:")
    print(f"ID: {first_certificate_id}")
    print(f"Issuer: {certificate_info.Issuer}")
    print(f"Subject: {certificate_info.Subject}")
    print(f"Valid From: {certificate_info.ValidFrom}")
    print(f"Valid To: {certificate_info.ValidTo}")
else:
    print("No certificates found.")
