import cv2
import requests
import numpy as np

# Camera Credentials
CAMERA_IP = "14.195.152.243"  # Replace with your camera IP
USERNAME = "admin"  # Replace with your camera username
PASSWORD = "admin@123"  # Replace with your camera password

# HTTP MJPEG Stream URL (Check Camera Documentation)
STREAM_URL = f"http://{USERNAME}:{PASSWORD}@{CAMERA_IP}/mjpeg"

# Open the MJPEG Stream
print(f"Connecting to MJPEG stream: {STREAM_URL}")

stream = requests.get(STREAM_URL, stream=True)
if stream.status_code != 200:
    print("Error: Cannot connect to MJPEG stream")
    exit()

print("Streaming Live Video... Press 'Q' to exit.")

byte_buffer = b""
for chunk in stream.iter_content(chunk_size=1024):
    byte_buffer += chunk
    a = byte_buffer.find(b"\xff\xd8")  # JPEG start
    b = byte_buffer.find(b"\xff\xd9")  # JPEG end
    
    if a != -1 and b != -1:
        jpg = byte_buffer[a:b+2]
        byte_buffer = byte_buffer[b+2:]

        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

        if frame is not None:
            cv2.imshow("MJPEG Camera Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting live stream...")
            break

cv2.destroyAllWindows()


