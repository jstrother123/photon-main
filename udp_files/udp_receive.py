import socket

HOST = "0.0.0.0" # listen to all incoming addresses
PORT = 7501
BUFFER_SIZE = 4096  

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Allow quick restart of the program
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((HOST, PORT))

print(f"Listening for UDP on {HOST}:{PORT}...")

while True:
    try:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        print(f"From {addr}: {data.decode(errors='ignore')}")
    except KeyboardInterrupt:
        print("\nShutting down.")
        break

sock.close()
