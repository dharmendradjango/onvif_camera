from onvif import ONVIFCamera


CAMERA_IP = "14.195.152.243"
PORT = 80
USERNAME = "admin"
PASSWORD = "admin@123"


camera = ONVIFCamera(CAMERA_IP, PORT, USERNAME, PASSWORD)


media_service = camera.create_media_service()


profiles = media_service.GetProfiles()


print("\n🔹 Available Profiles:")
for i, p in enumerate(profiles):
    print(f"Profile {i}: Token = {p.token}")
    if p.VideoEncoderConfiguration:
        print(f"  Encoder Token: {p.VideoEncoderConfiguration.token}")
    else:
        print("  ❌ No VideoEncoderConfiguration")


profile_index = 4
if profile_index >= len(profiles):
    print(f"❌ Error: Profile index {profile_index} is out of range!")
    exit()

profile = profiles[profile_index]


video_encoder_config = profile.VideoEncoderConfiguration


if not video_encoder_config:
    print("⚠️ Profile has no VideoEncoderConfiguration, trying GetVideoEncoderConfigurations()")
    video_encoder_configs = media_service.GetVideoEncoderConfigurations()
    if video_encoder_configs:
        video_encoder_config = video_encoder_configs[0]  # Use the first available configuration
    else:
        print("❌ No Video Encoder Configurations found!")
        exit()


video_encoder_config.Resolution.Width = 2480   
video_encoder_config.Resolution.Height = 1120   
video_encoder_config.RateControl.FrameRateLimit = 30  
video_encoder_config.Encoding = "H264"  


video_config_request = media_service.create_type('SetVideoEncoderConfiguration')
video_config_request.ForcePersistence = True
video_config_request.Configuration = video_encoder_config


media_service.SetVideoEncoderConfiguration(video_config_request)

print("✅ Video configuration updated successfully!")













# import cv2
# import requests
# import numpy as np
# from flask import Flask, Response

# # Camera Credentials
# CAMERA_IP = "14.195.152.243"  
# USERNAME = "admin"  
# PASSWORD = "admin@123"  

# # MJPEG Stream URL
# STREAM_URL = f"http://{USERNAME}:{PASSWORD}@{CAMERA_IP}/mjpeg"

# # Initialize Flask
# app = Flask(__name__)

# def generate_frames():
#     """Capture frames from MJPEG stream and serve them via Flask."""
#     print(f"Connecting to MJPEG stream: {STREAM_URL}")
#     try:
#         stream = requests.get(STREAM_URL, stream=True, timeout=10)
#         if stream.status_code != 200:
#             print("Error: Cannot connect to MJPEG stream")
#             return

#         byte_buffer = b""
#         for chunk in stream.iter_content(chunk_size=1024):
#             byte_buffer += chunk
#             a = byte_buffer.find(b"\xff\xd8")  # JPEG Start
#             b = byte_buffer.find(b"\xff\xd9")  # JPEG End

#             if a != -1 and b != -1:
#                 jpg = byte_buffer[a:b+2]
#                 byte_buffer = byte_buffer[b+2:]

#                 frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

#                 if frame is not None:
#                     _, buffer = cv2.imencode('.jpg', frame)
#                     frame_bytes = buffer.tobytes()
#                     yield (b'--frame\r\n'
#                         b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching video stream: {e}")

# @app.route('/video')
# def video_feed():
#     """Serve the live video feed."""
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     print("Starting Flask server... Open http://14.195.152.243:8080/video to watch the stream.")
#     app.run(host='0.0.0.0', port=8080, debug=True)
