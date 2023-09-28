#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 7500 // Port number to send the broadcast
#define NETWORK_ADDRESS "192.168.1.255" // Replace with your specific network address

int main() {
    int sockfd;
    struct sockaddr_in broadcast_addr;
    char broadcast_message[] = "Hello, UDP Broadcast!";
    
    // Create a UDP socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd == -1) {
        printf("unable to create socket\n");
        exit(1);
    }
    
    // Set socket options to allow broadcast
    int broadcast_enable = 1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, &broadcast_enable, sizeof(broadcast_enable)) == -1 ) {
        printf("unable to enable broadcasts\n");
        exit(1);
    }
    
    // Initialize the broadcast address structure
    memset(&broadcast_addr, 0, sizeof(broadcast_addr));
    broadcast_addr.sin_family = AF_INET;
    broadcast_addr.sin_port = htons(PORT);
    if (inet_pton(AF_INET, NETWORK_ADDRESS, &broadcast_addr.sin_addr) <= 0) {
        perror("inet_pton");
        exit(1);
    }
    
    // Send the broadcast message
    ssize_t bytes_sent = sendto(sockfd, broadcast_message, strlen(broadcast_message), 0,
                                (struct sockaddr*)&broadcast_addr, sizeof(broadcast_addr));
    
    if (bytes_sent == -1) {
        perror("sendto");
    } else {
        printf("Sent %ld bytes to %s:%d\n", bytes_sent, NETWORK_ADDRESS, PORT);
    }
    
    close(sockfd);
    return 0;
}

