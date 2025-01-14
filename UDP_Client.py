import socket
import json

# Call the method and pass in the info that user entered
def passInfo(id):
	# Player's info
	msgFromClient      = str(id)
	bytesToSend        = str.encode(msgFromClient)
	#print(msgFromClient)
	
	# Client's info
	clientAddressPort   = ("127.0.0.1", 7500)
	bufferSize          = 1024
	
	# Create a UDP socket at client side
	UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	
	try:
		# Send the user's info
		UDPClientSocket.sendto(bytesToSend, clientAddressPort)
		
	except socket.error as e:
		print(f"Socket error: {e}")
		
	finally:
		# Close the client socket
		if UDPClientSocket:
			UDPClientSocket.close()

# Test
# passInfo(1, "John", 23)
