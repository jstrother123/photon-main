import socket
import time

SOURCE_IP = "127.0.0.1"     # Your local interface ( I will use 192.168.1.2)
PORT = 7500
BROADCAST_IP = "127.0.0.255"  # for testing with the hardware, I will use 192.168.1.255
MESSAGE = "Hello UDP broadcast"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Allow broadcasting
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


print(f"Broadcasting from {SOURCE_IP} to {BROADCAST_IP}:{PORT}")

while True:
    sock.sendto(MESSAGE.encode(), (BROADCAST_IP, PORT))
    print("Sent:", MESSAGE)
    time.sleep(1)  # send every 1 second
