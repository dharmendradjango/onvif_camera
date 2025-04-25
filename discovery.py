import socket
import struct
import time

# WS-Discovery probe message XML template
PROBE_MESSAGE = '''<?xml version="1.0" encoding="UTF-8"?>
<Probe xmlns="http://schemas.xmlsoap.org/ws/2005/04/discovery">
    <Types>dn:NetworkVideoTransmitter</Types>
    <Scopes>onvif://www.onvif.org/Profile/Streaming</Scopes>
</Probe>'''

# Multicast address and port for WS-Discovery
MULTICAST_ADDRESS = '239.255.255.250'
MULTICAST_PORT = 3702

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)  # Set the multicast TTL

# Set the timeout for the socket
sock.settimeout(5)  # 5 seconds to wait for responses

# Send Probe message to the multicast group
sock.sendto(PROBE_MESSAGE.encode('utf-8'), (MULTICAST_ADDRESS, MULTICAST_PORT))

print(f"Sent Probe message to {MULTICAST_ADDRESS}:{MULTICAST_PORT}")

# Listen for responses
try:
    while True:
        data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        print(f"Received ProbeMatch response from {addr}")
        print(f"Response data: {data.decode('utf-8')}")
        time.sleep(1)  # Wait a bit before receiving next response
except socket.timeout:
    print("No responses received within timeout.")

# Close the socket after communication is done
sock.close()
