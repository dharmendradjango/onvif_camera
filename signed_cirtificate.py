from onvif import ONVIFCamera
from datetime import datetime, timedelta


camera_ip = "115.242.203.134"  
username = "admin"           
password = "admin@123"        
port = 80                   

try:
    
    camera = ONVIFCamera(camera_ip, port, username, password)

   
    device_service = camera.create_devicemgmt_service()

    # Set up certificate parameters
    certificate_id = "SelfSigned1"
    subject = {
        "Country": "US",
        "Organization": "MyOrganization",
        "CommonName": "MyDevice"
    }  

    # Set certificate validity period
    valid_not_before = datetime.utcnow()
    valid_not_after = valid_not_before + timedelta(days=365)  # 1 year validity

    # Convert datetime to the required format for ONVIF
    def convert_to_gmt(date_time):
        return {
            "Year": date_time.year,
            "Month": date_time.month,
            "Day": date_time.day,
            "Hour": date_time.hour,
            "Minute": date_time.minute,
            "Second": date_time.second
        }

    valid_not_before_gmt = convert_to_gmt(valid_not_before)
    valid_not_after_gmt = convert_to_gmt(valid_not_after)

    # Create the self-signed certificate
    nvt_certificate = device_service.CreateCertificate(
        CertificateID=certificate_id,
        Subject=subject,
        ValidNotBefore=valid_not_before_gmt,
        ValidNotAfter=valid_not_after_gmt
    )
    print(f"Created Certificate ID: {nvt_certificate.CertificateID}")

    # Get the status of all device certificates
    certificate_statuses = device_service.GetCertificatesStatus()

    # Enable the new certificate and disable others
    for cert_status in certificate_statuses:
        if cert_status.CertificateID == nvt_certificate.CertificateID:
            cert_status.Status = True  # Enable the new certificate
        else:
            cert_status.Status = False  # Disable all other certificates

    # Apply the updated certificate statuses
    device_service.SetCertificatesStatus(certificate_statuses)
    print("Updated certificate statuses successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
