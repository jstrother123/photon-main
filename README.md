# photon-main
Main software for Photon Laser Tag

python main.py to run the application

UDP:
The server will keep listening to the client and store the players' information in the JSON file called players_score.

import UDP_Client # Add in the head of the main.py

# When passing info to the database, also call the udp client to transfer info to server
UDP_Client.passInfo(id, playerName, equipId)
