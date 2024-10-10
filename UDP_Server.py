import socket
import json
import os

localIP = "127.0.0.1"
#localPort = 20001
localPort = 7501
bufferSize = 1024
msgFromServer = "Hello UDP Client, data has been received"
bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Json file path
file_path = 'players_score.json'

# Check if the file exist or not, if not, create the file
if not os.path.exists(file_path):
    players_data = {}
    with open(file_path, 'w') as file:
        json.dump(players_data, file)

# Listen for incoming datagrams
while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    # Load the file already exist
    with open(file_path, 'r') as file:
        players_data = json.load(file)

    try:
        decoded_message = message.decode('utf-8')
        player_info = json.loads(decoded_message)

        player_id = player_info.get("id")
        player_name = player_info.get("name")
        player_equipNum = player_info.get("equipNum")

        # Insert or update the user's data
        players_data[player_name] = {
            "id": player_id,
            "equipNum": player_equipNum
        }

        # Save the data after updated
        with open(file_path, 'w') as file:
            json.dump(players_data, file, indent=4)

        print(f"Updated player data: {players_data}")

    except json.JSONDecodeError:
        print("Failed to decode JSON from client")

    except Exception as e:
        print(f"An error occurred: {e}")

    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)
