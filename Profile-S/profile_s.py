from onvif import ONVIFCamera
import cv2


IP = "14.195.152.243"  
PORT = 80  
USER = "admin"  
PASSWORD = "admin@123"  


camera = ONVIFCamera(IP, PORT, USER, PASSWORD)

media_service = camera.create_media_service()

profiles = media_service.GetProfiles()
profile_token = profiles[6].token  


stream_request = media_service.create_type('GetStreamUri')
stream_request.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
stream_request.ProfileToken = profile_token
stream_uri = media_service.GetStreamUri(stream_request)


rtsp_url = stream_uri.Uri.replace("rtsp://", f"rtsp://{USER}:{PASSWORD}@")
print(f"RTSP Stream URL: {rtsp_url}")


cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Error: Unable to open video stream.")
    exit()


while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to retrieve frame")
        break

    cv2.imshow("ONVIF Camera Stream (Profile S)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
