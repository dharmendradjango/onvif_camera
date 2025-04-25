from onvif import ONVIFCamera
import time

# Device connection details
# device_ip = "115.245.98.54"
device_ip = '14.195.152.243' 
device_port = 80             
username = "admin"          
password = "admin@123"        


client = ONVIFCamera(device_ip, device_port, username, password)


device_service = client.create_devicemgmt_service()


network_protocols = device_service.GetNetworkProtocols()
for network_protocol in network_protocols:
    if network_protocol.Name == "HTTPS":
        network_protocol.Enabled = True
        network_protocol.Port[0] = 443  # Set HTTPS port to 443
device_service.SetNetworkProtocols(network_protocols)

# Step 2: Wait for the device to apply changes (e.g., reboot)
# print("Waiting for the device to reboot...")
# time.sleep(120)  

# Step 3: Start TLS connection
# Once HTTPS is enabled, we need to ensure that all further connections use TLS
client.start_tls()

# Access the media service for streaming
media_service = client.create_media_service()

# Step 4: Retrieve available profiles and choose the first one
profile_list = media_service.GetProfiles()
target_profile_token = profile_list[2].token  # Use the first profile

# Step 5: Set up Stream URI parameters
stream_setup = {
    'Stream': 'RTP-Unicast',  # Unicast streaming type (could also be RTP-Multicast)
    'Transport': {
        'Protocol': 'RTSP',  # Set RTSP for the transport protocol
        'Tunnel': None  # No tunnel required for RTSP
    }
}

# Step 6: Get the HTTPS stream URI
try:
    media_uri = media_service.GetStreamUri(StreamSetup=stream_setup, ProfileToken=target_profile_token)
    print(f"RTSP over HTTPS URI: {media_uri.Uri}")
except Exception as e:
    print(f"Error retrieving stream URI: {e}")
    exit()

# Step 7: Start streaming (pass the URI to your streaming application)
# For example, using OpenCV or another method to view the stream
# App.DoStreaming(media_uri.Uri)

# For this example, we'll just simulate streaming by printing the URI
print(f"Streaming started: {media_uri.Uri}")

# Step 8: Stop streaming
# In real use, you'd have a mechanism to stop the streaming once done
# App.StopStreaming(media_uri.Uri)

# Step 9: End the TLS connection
client.stop_tls()

# Final message to indicate completion
print("Streaming stopped and TLS connection closed.")
