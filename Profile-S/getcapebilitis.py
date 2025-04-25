from onvif import ONVIFCamera

# Auto-discover ONVIF cameras on the network
camera = ONVIFCamera("14.195.152.243", 80, "admin", "admin@123")
print(camera.devicemgmt.GetCapabilities())




# from onvif import ONVIFCamera
# import argparse

# def get_onvif_data(ip, port, user, password):
#     """
#     Retrieves ONVIF Profile S data from a camera.

#     Args:
#         ip: IP address of the camera.
#         port: Port number (usually 80 or 8080).
#         user: Username for authentication.
#         password: Password for authentication.
#     """
#     try:
#         mycam = ONVIFCamera(ip, port, user, password)

#         # Get media service
#         media = mycam.create_media_service()

#         # Get profiles
#         profiles = media.GetProfiles()

#         if profiles:
#             for profile in profiles:
#                 print(f"Profile Token: {profile.token}")
#                 # Get stream URIs
#                 stream_uris = media.GetStreamUri({'ProfileToken': profile.token, 'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}})
#                 print(f"Stream URI: {stream_uris.Uri}")

#         # Get device information
#         devicemgmt = mycam.create_devicemgmt_service()
#         device_info = devicemgmt.GetDeviceInformation()
#         print("\nDevice Information:")
#         print(f"Manufacturer: {device_info.Manufacturer}")
#         print(f"Model: {device_info.Model}")
#         print(f"FirmwareVersion: {device_info.FirmwareVersion}")
#         print(f"SerialNumber: {device_info.SerialNumber}")
#         print(f"HardwareId: {device_info.HardwareId}")

#         # Get PTZ capabilities and status (if available)
#         try:
#             ptz = mycam.create_ptz_service()
#             ptz_capabilities = ptz.GetCapabilities({'ProfileToken': profiles[0].token})
#             print("\nPTZ Capabilities:", ptz_capabilities)
#             ptz_status = ptz.GetStatus({'ProfileToken': profiles[0].token})
#             print("\nPTZ Status:", ptz_status)
#         except Exception as ptz_error:
#             print(f"\nPTZ Error or PTZ not available: {ptz_error}")

#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     # Directly call the function with the provided credentials.
#     get_onvif_data("14.195.152.243", 80, "admin", "admin@123")