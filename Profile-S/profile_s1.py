from onvif import ONVIFCamera
import cv2


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
    exit()

profile_token = profiles[1].token
print(f"[INFO] Using Profile Token: {profile_token}")

stream_request = media_service.create_type('GetStreamUri')
stream_request.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
stream_request.ProfileToken = profile_token
stream_uri = media_service.GetStreamUri(stream_request)

rtsp_url = stream_uri.Uri.replace("rtsp://", f"rtsp://{USER}:{PASSWORD}@")
print(f"[INFO] RTSP Stream URL: {rtsp_url}")

print("[INFO] Opening video stream...")
cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("[ERROR] Unable to open video stream. Check your credentials and RTSP settings.")
    exit()

print("[INFO] Streaming live video. Press 'Q' to exit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Failed to retrieve frame")
        break

    cv2.imshow("ONVIF Camera Stream (Profile S)", frame)
  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("[INFO] Stream closed successfully.")
