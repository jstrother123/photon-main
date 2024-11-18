import socket
import json

# Call the method and pass in the info that user entered
def passInfo(id, name, equipNum, team):
    try:
        # Greeting
        msgFromClient1 = "Hello UDP Sever, here's the user data"
        bytesToSend1 = str.encode(msgFromClient1)

        # Player's info
        msgFromClient2      = f"{id},{name},{equipNum},{team}"
        msgFromClient2      = json.dumps({"id": id, "name": name, "equipNum": equipNum, "team": team})
        bytesToSend2        = str.encode(msgFromClient2)
        #print(msgFromClient2)
        #print("Receive from main")

        # Server's info
        serverAddressPort   = ("127.0.0.1", 7500)
        bufferSize          = 1024

        # Create a UDP socket at client side
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Send the msg to server using created UDP socket
        UDPClientSocket.sendto(bytesToSend1, serverAddressPort)
        
        # Receiving
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = "Message from Server {}".format(msgFromServer[0])
        #print(msg)

        # Send the user's info
        UDPClientSocket.sendto(bytesToSend2, serverAddressPort)
        #print("Successully send.")

        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = "Message from Server {}".format(msgFromServer[0])
        #print(msg)

    except socket.error as e:
        print(f"Socket error: {e}")

    finally:
        # Close the client socket
        UDPClientSocket.close()

# Test
# passInfo(1, "John", 23)
