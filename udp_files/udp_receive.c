#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 7500 // Specify the UDP port you want to listen on

int main() {
    int sockfd;
    struct sockaddr_in my_addr;
    struct sockaddr_in client_addr;
    socklen_t addr_len = sizeof(struct sockaddr_in);
    char buffer[1024];

    // Create a UDP socket
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
        perror("socket");
        exit(1);
    }

    // Fill in the server's sockaddr_in structure
    memset(&my_addr, 0, sizeof(my_addr));
    my_addr.sin_family = AF_INET;
    my_addr.sin_port = htons(PORT);
	my_addr.sin_addr.s_addr = INADDR_ANY;  // listen on all network interfaces
	
    // Bind the socket to the specified address and port
    if (bind(sockfd, (struct sockaddr*)&my_addr, sizeof(my_addr)) == -1) {
        perror("bind");
        exit(1);
    }

    printf("Listening for UDP broadcasts on %d...\n", PORT);

    while (1) {
        // Receive data from clients
        ssize_t num_bytes = recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr*)&client_addr, &addr_len);
        if (num_bytes == -1) {
            perror("recvfrom");
            exit(1);
        }

        // Print the received data
        buffer[num_bytes] = '\0'; // Null-terminate the received data
        printf("Received from %s:%d: %s\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port), buffer);
    }

    // Close the socket
    close(sockfd);

    return 0;
}
