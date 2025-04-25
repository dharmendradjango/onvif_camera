from onvif import ONVIFCamera
import cv2
import zeep
import time
import threading
import numpy as np

IP = "14.195.152.243"  
PORT = 80  
USER = "admin"  
PASSWORD = "admin@123"  

print("[INFO] Connecting to ONVIF camera...")
camera = ONVIFCamera(IP, PORT, USER, PASSWORD)


zeep.xsd.simple.AnySimpleType.pythonvalue = lambda self, value: value


media_service = camera.create_media_service()

print("[INFO] Fetching available profiles...")
profiles = media_service.GetProfiles()

if not profiles:
    print("[ERROR] No ONVIF profiles found on the camera!")
    exit()

profile_token = profiles[16].token
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


fgbg = cv2.createBackgroundSubtractorMOG2()

def detect_motion(frame):
    fgmask = fgbg.apply(frame)
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 500:  
            print("[ALERT] Motion detected!")
            return True
    return False


def event_listener():
    try:
        print("[INFO] Subscribing to motion detection events...")
        event_service = camera.create_events_service()
        
        
        pullpoint_response = event_service.CreatePullPointSubscription()
        pullpoint_url = pullpoint_response.SubscriptionReference.Address  
        
        
        pullpoint_service = camera.create_pullpoint_service(pullpoint_url)

        while True:
            time.sleep(5)  
            try:
                messages = pullpoint_service.PullMessages({
                    'Timeout': 60,
                    'MessageLimit': 5
                })
                if messages and messages.NotificationMessage:
                    for msg in messages.NotificationMessage:
                        print(f"[EVENT] ONVIF Event detected: {msg}")
                        if "Motion" in str(msg):  
                            print("[ALERT] Motion detected via ONVIF event!")
            except Exception as e:
                print(f"[ERROR] Failed to pull messages: {e}")
                break
    except Exception as e:
        print(f"[ERROR] Event listener setup failed: {e}")


event_thread = threading.Thread(target=event_listener, daemon=True)
event_thread.start()


print("[INFO] Streaming live video. Press 'Q' to exit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Failed to retrieve frame")
        break
    
    if detect_motion(frame):
        print("[ALERT] Motion detected in video feed!")
    
    cv2.imshow("ONVIF Camera Stream (Profile S)", frame)
  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("[INFO] Stream closed successfully.")













# from onvif import ONVIFCamera
# import cv2
# import zeep
# import time
# import threading

# IP = "14.195.152.243"  
# PORT = 80  
# USER = "admin"  
# PASSWORD = "admin@123"  

# print("[INFO] Connecting to ONVIF camera...")
# camera = ONVIFCamera(IP, PORT, USER, PASSWORD)

# # Fixing ONVIF compatibility issue
# zeep.xsd.simple.AnySimpleType.pythonvalue = lambda self, value: value

# # Media service setup
# media_service = camera.create_media_service()

# print("[INFO] Fetching available profiles...")
# profiles = media_service.GetProfiles()

# if not profiles:
#     print("[ERROR] No ONVIF profiles found on the camera!")
#     exit()

# profile_token = profiles[0].token
# print(f"[INFO] Using Profile Token: {profile_token}")

# # Get RTSP stream URL
# stream_request = media_service.create_type('GetStreamUri')
# stream_request.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
# stream_request.ProfileToken = profile_token
# stream_uri = media_service.GetStreamUri(stream_request)

# rtsp_url = stream_uri.Uri.replace("rtsp://", f"rtsp://{USER}:{PASSWORD}@")
# print(f"[INFO] RTSP Stream URL: {rtsp_url}")

# # OpenCV Video Capture
# print("[INFO] Opening video stream...")
# cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

# if not cap.isOpened():
#     print("[ERROR] Unable to open video stream. Check your credentials and RTSP settings.")
#     exit()

# # Event handling for motion detection
# def event_listener():
#     try:
#         print("[INFO] Subscribing to motion detection events...")
#         event_service = camera.create_events_service()
        
#         # Create PullPointSubscription
#         pullpoint_response = event_service.CreatePullPointSubscription()
#         pullpoint_url = pullpoint_response.SubscriptionReference.Address  # Get pull-point URL
        
#         # Connect to the pull-point service
#         pullpoint_service = camera.create_pullpoint_service(pullpoint_url)

#         while True:
#             time.sleep(5)  # Polling interval
#             try:
#                 messages = pullpoint_service.PullMessages({
#                     'Timeout': 60,
#                     'MessageLimit': 5
#                 })
#                 if messages and messages.NotificationMessage:
#                     for msg in messages.NotificationMessage:
#                         if "Motion" in str(msg):  # Check for motion events
#                             print("[ALERT] Motion detected!")
#             except Exception as e:
#                 print(f"[ERROR] Failed to pull messages: {e}")
#                 break
#     except Exception as e:
#         print(f"[ERROR] Event listener setup failed: {e}")

# # Run event listener in a separate thread
# event_thread = threading.Thread(target=event_listener, daemon=True)
# event_thread.start()

# # Stream video
# print("[INFO] Streaming live video. Press 'Q' to exit.")
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("[ERROR] Failed to retrieve frame")
#         break

#     cv2.imshow("ONVIF Camera Stream (Profile S)", frame)
  
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
# print("[INFO] Stream closed successfully.")
