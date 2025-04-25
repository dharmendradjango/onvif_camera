
import cv2
import subprocess
import threading
import socket
import pyaudio
from onvif import ONVIFCamera

CAMERA_IP = "14.195.152.243"  
USERNAME = "admin"  
PASSWORD = "admin@123"  
PORT = 554  

stream_uri = f"rtsp://{USERNAME}:{PASSWORD}@{CAMERA_IP}:{PORT}/cam/realmonitor?channel=4&subtype=0&unicast=true&proto=Onvif"
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

cap = cv2.VideoCapture(stream_uri)

def display_video():
    """Display video stream in a window while recording."""
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow('ONVIF Camera Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

AUDIO_IP = "0.0.0.0"  
AUDIO_PORT = 12345  

def udp_audio_stream():
    """Receive and play audio via UDP with low latency."""
    FORMAT = pyaudio.paInt16
    CHUNK = 1024  # Reduce if needed for lower latency
    CHANNELS = 2
    RATE = 44100
    BUFFER_SIZE = 10000 # Increase buffer size for faster audio capture

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT, 
        channels=CHANNELS, 
        rate=RATE, 
        output=True, 
        frames_per_buffer=CHUNK,
        stream_callback=None  # Avoid extra processing delays
    )

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((AUDIO_IP, AUDIO_PORT))
    udp_socket.setblocking(False)  # Non-blocking mode to reduce delays

    print("Listening for audio stream...")

    while True:
        try:
            sound_data, _ = udp_socket.recvfrom(BUFFER_SIZE)
            if sound_data:
                stream.write(sound_data, CHUNK)  # Play audio with lower latency
        except BlockingIOError:
            continue  # Avoid waiting if no data is available

    udp_socket.close()
    stream.stop_stream()
    stream.close()
    audio.terminate()

video_thread = threading.Thread(target=display_video)
audio_thread = threading.Thread(target=udp_audio_stream)

video_thread.start()
audio_thread.start()

video_thread.join()
audio_thread.join()

ffmpeg_process.terminate()

cap.release()
cv2.destroyAllWindows()
