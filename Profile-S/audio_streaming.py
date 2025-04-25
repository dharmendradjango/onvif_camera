# from onvif import ONVIFCamera
# import cv2
# import pyaudio
# import threading
# import ffmpeg

# IP = "14.195.152.243"  
# PORT = 80  
# USER = "admin"  
# PASSWORD = "admin@123"  

# print("[INFO] Connecting to ONVIF camera...")
# camera = ONVIFCamera(IP, PORT, USER, PASSWORD)

# media_service = camera.create_media_service()

# print("[INFO] Fetching available profiles...")
# profiles = media_service.GetProfiles()

# if not profiles:
#     print("[ERROR] No ONVIF profiles found on the camera!")
#     exit()

# profile_token = profiles[1].token
# print(f"[INFO] Using Profile Token: {profile_token}")

# stream_request = media_service.create_type('GetStreamUri')
# stream_request.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
# stream_request.ProfileToken = profile_token
# stream_uri = media_service.GetStreamUri(stream_request)

# rtsp_url = stream_uri.Uri.replace("rtsp://", f"rtsp://{USER}:{PASSWORD}@")
# print(f"[INFO] RTSP Stream URL: {rtsp_url}")

# audio_url = rtsp_url.replace("video", "audio")  # Assuming ONVIF provides an audio stream

# # Function to stream audio
# def stream_audio():
#     print("[INFO] Starting audio stream...")
#     try:
#         process = (
#             ffmpeg
#             .input(audio_url)
#             .output('pipe:', format='wav')
#             .run_async(pipe_stdout=True, pipe_stderr=True)
#         )
#         p = pyaudio.PyAudio()
#         stream = p.open(format=p.get_format_from_width(2), channels=1, rate=50000, output=True)
#         while True:
#             data = process.stdout.read(2024)
#             if not data:
#                 break
#             stream.write(data)
#     except Exception as e:
#         print(f"[ERROR] Audio streaming failed: {e}")

# audio_thread = threading.Thread(target=stream_audio, daemon=True)
# audio_thread.start()

# print("[INFO] Opening video stream...")
# cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

# if not cap.isOpened():
#     print("[ERROR] Unable to open video stream. Check your credentials and RTSP settings.")
#     exit()

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





import subprocess
import threading
import socket
import pyaudio


CAMERA_IP = "14.195.152.243"
USERNAME = "admin"
PASSWORD = "admin@123"
PORT = 554


stream_uri = f"rtsp://{USERNAME}:{PASSWORD}@{CAMERA_IP}:{PORT}/cam/realmonitor?channel=2&subtype=0&unicast=true&proto=Onvif"
print(f"RTSP Stream URL: {stream_uri}")


output_file = "camera_recording.mp4"


ffmpeg_command = [
    "ffmpeg",
    "-rtsp_transport", "tcp",
    "-i", stream_uri,
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "128k",
    "-f", "mp4",
    output_file
]


ffmpeg_process = subprocess.Popen(ffmpeg_command)

def udp_audio_stream():
    """Receive and play audio via UDP."""
    FORMAT = pyaudio.paInt16
    CHUNK = 1024
    CHANNELS = 2
    RATE = 44100

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", 12345))

    print("Listening for audio stream...")

    try:
        while True:
            sound_data, _ = udp_socket.recvfrom(CHUNK * CHANNELS * 2)
            stream.write(sound_data)
    except KeyboardInterrupt:
        pass
    finally:
        udp_socket.close()
        stream.stop_stream()
        stream.close()
        audio.terminate()


audio_thread = threading.Thread(target=udp_audio_stream)
audio_thread.start()


audio_thread.join()


ffmpeg_process.terminate()




# import cv2
# import subprocess
# import threading
# import socket
# import pyaudio
# from onvif import ONVIFCamera


# CAMERA_IP = "14.195.152.243"  
# USERNAME = "admin"  
# PASSWORD = "admin@123"  
# PORT = 554  


# stream_uri = f"rtsp://{USERNAME}:{PASSWORD}@{CAMERA_IP}:{PORT}/cam/realmonitor?channel=2&subtype=0&unicast=true&proto=Onvif"
# print(f"RTSP Stream URL: {stream_uri}")


# output_file = "camera_recording.mp4"


# ffmpeg_command = [
#     "ffmpeg",
#     "-rtsp_transport", "tcp",
#     "-i", stream_uri,  
#     "-c:v", "copy",    
#     "-c:a", "aac",     
#     "-b:a", "128k",    
#     "-f", "mp4",       
#     output_file
# ]


# ffmpeg_process = subprocess.Popen(ffmpeg_command)


# cap = cv2.VideoCapture(stream_uri)

# def display_video():
#     """Display video stream in a window while recording."""
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if ret:
#             cv2.imshow('ONVIF Camera Stream', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break


# AUDIO_IP = "0.0.0.0"  
# AUDIO_PORT = 12345  
# def udp_audio_stream():
#     """Receive and play audio via UDP."""
#     FORMAT = pyaudio.paInt16
#     CHUNK = 1024
#     CHANNELS = 2
#     RATE = 44100

#     audio = pyaudio.PyAudio()
#     stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

#     udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udp_socket.bind((AUDIO_IP, AUDIO_PORT))

#     print("Listening for audio stream...")

#     while True:
#         sound_data, _ = udp_socket.recvfrom(CHUNK * CHANNELS * 2)
#         stream.write(sound_data)

#     udp_socket.close()
#     stream.stop_stream()
#     stream.close()
#     audio.terminate()


# video_thread = threading.Thread(target=display_video)
# audio_thread = threading.Thread(target=udp_audio_stream)

# video_thread.start()
# audio_thread.start()


# video_thread.join()
# audio_thread.join()


# ffmpeg_process.terminate()


# cap.release()
# cv2.destroyAllWindows()
