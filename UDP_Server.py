import socket
import json
import os
import UDP_Client
from UDP_Client import passInfo
import GameActionScreen
from GameActionScreen import scoring
from GameActionScreen import greenGotBase
from GameActionScreen import redGotBase


serverIP = "127.0.0.1"
serverPort = 7501
bufferSize = 1024
clientPort = 7500

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((serverIP, serverPort))

print("UDP server up and listening")

# Listen for incoming datagrams
while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    playerId = message.decode('utf-8')
    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)
    
    #print(message)
    #print(clientMsg)
    #print(clientIP)
    
    # Once the game starts
    try: 
        id1, id2 = map(int, playerId.split(":"))
        #id1, id2 = clientMsg.split(":")
        #print(id1, id2)
			
        # Green hitting base
        if (id2 == 53):
            greenGotBase(id1)
            #print("Green just hit the base!")
            passInfo(id1)
            
        # Red hitting base
        elif (id2 == 43):
            redGotBase(id1)
            #print("Red just hit the base!")
            passInfo(id1)
            
        # Scoring, id2 got hit
        else:
            scoring(id1, id2)
            passInfo(id2)
            
    except ValueError:
        print("Invalid message format, skipping...")
    
# Close the server socket
UDPServerSocket.close()
