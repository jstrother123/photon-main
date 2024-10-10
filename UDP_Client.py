import socket
import json

# Call the method and pass in the info that user entered
def passInfo(id, name, equipNum):
    try:
        # Greeting
        msgFromClient1 = "Hello UDP Sever, here's the user data"
        bytesToSend1 = str.encode(msgFromClient1)

        # Player's info
        #msgFromClient2 = f"{id},{name},{equipNum}"
        msgFromClient2 = json.dumps({"id": id, "name": name, "equipNum": equipNum})
        bytesToSend2        = str.encode(msgFromClient2)

        # Server's info
        serverAddressPort   = ("127.0.0.1", 7501)
        bufferSize          = 1024

        # Create a UDP socket at client side
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Send the greeting msg to server using created UDP socket
        UDPClientSocket.sendto(bytesToSend1, serverAddressPort)
        # Receive the response
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = "Message from Server {}".format(msgFromServer[0])

        print(msg)

        # Send the user's info
        UDPClientSocket.sendto(bytesToSend2, serverAddressPort)

        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = "Message from Server {}".format(msgFromServer[0])

        print(msg)

    except socket.error as e:
        print(f"Socket error: {e}")

    finally:
        # Close the client socket
        UDPClientSocket.close()

# Test
# passInfo(1, "John", 23)
