# from onvif import ONVIFCamera
# import sys
# import webbrowser

# # Camera Details
# IP = "14.195.152.243"
# PORT = 80
# USER = "admin"
# PASSWORD = "admin@123"

# print("[INFO] Connecting to ONVIF camera...")
# camera = ONVIFCamera(IP, PORT, USER, PASSWORD)

# # Get Media Service
# media_service = camera.create_media_service()

# print("[INFO] Fetching available profiles...")
# profiles = media_service.GetProfiles()

# if not profiles:
#     print("[ERROR] No ONVIF profiles found on the camera!")
#     sys.exit()

# # Select the first available Profile S Compatible Stream
# profile = profiles[7]  # Using first profile
# profile_token = profile.token
# print(f"[INFO] Using Profile Token: {profile_token}")

# # Get HTTP MJPEG Stream URI
# stream_request = media_service.create_type('GetStreamUri')
# stream_request.StreamSetup = {
#     'Stream': 'RTP-Unicast',
#     'Transport': {'Protocol': 'HTTP'}
# }
# stream_request.ProfileToken = profile_token
# stream_uri = media_service.GetStreamUri(stream_request)

# mjpeg_url = stream_uri.Uri.replace("http://", f"http://{USER}:{PASSWORD}@")
# print(f"[INFO] MJPEG Stream URL: {mjpeg_url}")

# # Open in Web Browser
# print("[INFO] Opening camera stream in browser...")
# webbrowser.open(mjpeg_url)

# print("[INFO] Streaming started. Close browser to stop.")


from onvif import ONVIFCamera
import sys
import webbrowser


IP = "14.195.152.243"
PORT = 80
USER = "admin"
PASSWORD = "admin@123"

print("[INFO] Connecting to ONVIF camera...")
camera = ONVIFCamera(IP, PORT, USER, PASSWORD)

media_service = camera.create_media_service()

print("[INFO] Fetching available profiles...")
profiles = media_service.GetProfiles()

if not profiles:
    print("[ERROR] No ONVIF profiles found on the camera!")
    sys.exit()


profile_token = profiles[1].token if len(profiles) > 1 else profiles[0].token


stream_url = None
selected_profile = None
for profile in profiles:
    try:
        print(f"[INFO] Trying Profile: {profile.Name} (Token: {profile.token})")

        
        stream_request = media_service.create_type('GetStreamUri')
        stream_request.StreamSetup = {
            'Stream': 'RTP-Unicast',
            'Transport': {'Protocol': 'RTSP'}  
        }
        stream_request.ProfileToken = profile.token
        stream_uri = media_service.GetStreamUri(stream_request)

        
        if stream_uri and stream_uri.Uri:
            stream_url = stream_uri.Uri.replace("rtsp://", f"rtsp://{USER}:{PASSWORD}@")
            selected_profile = profile
            print(f"[SUCCESS] Found Stream: {stream_url} (Profile: {selected_profile.Name}, Token: {selected_profile.token})")
            break  

    except Exception as e:
        print(f"[ERROR] Failed with Profile {profile.Name}: {str(e)}")

if not stream_url:
    print("[ERROR] No valid H.264/H.265 stream found!")
    sys.exit()


print("[INFO] Streaming URL (open in a compatible player):")
print(stream_url)
print(f"[INFO] Selected Profile: {selected_profile.Name}, Token: {selected_profile.token}")
webbrowser.open(stream_url)
