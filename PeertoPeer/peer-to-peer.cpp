//Olivia Ennis and Amant Kaur
//EECE 446 - Spring 2022
//Program 3
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>
#include <arpa/inet.h>
#include <ctype.h>
#include <fcntl.h>
#include <fstream>

int lookup_and_connect( const char *host, const char *service );

//Source: Beejs Guide
//Sends all data from server
int send_all(int s, char* buf, int* bytes)
{
	int total = 0;
	int bytesleft = *bytes;
	int n;

	while (total < *bytes)
	{
		n = (send(s, buf + total, bytesleft, 0));
		if (n == -1)
		{
			break;
		}
		total += n;
		bytesleft -= n;
	}
	*bytes = total;

	return n == -1 ? -1 : 0;
}

//Source: based on send_all function from Beejs
//Receives a full chunk 
int receive_chunk(int s, char* buf, int* chunk_size)
{
	int total = 0;
	int bytesleft = *chunk_size;
	int n;

	while (total < *chunk_size)
	{
		n = recv(s, buf + total, bytesleft, 0);
		if (n == -1 || n == 0)
		{
			break;
		}
		total += n;
		bytesleft -= n;
	}
	*chunk_size = total;

	return total;
}

int main(int argc, char* argv[]) 
{
	//Puts user input into variables
	char *server = argv[1];
	char *port = argv[2];
	uint32_t peerID = atoi(argv[3]);
	uint32_t peerID_nbo = htonl(peerID);

	char input[50];
	int s;

	//Connects to server
	if ((s = lookup_and_connect(server, port)) < 0)
	{
		exit(1);
	}

	//Loops until connection closed
	bool connected = true;
	while (connected == true)
	{
		//Receive input from user
		printf("Enter a command: ");
		std::cin >> input;

		//If input is Join
		if (strcmp(input, "JOIN") == 0)
		{
			char message[5];

			//Inserts data into message
			message[0] = 0;
			memcpy(message+1, &peerID_nbo, sizeof(uint32_t));

			//Sends join request to server
			int len = 5;
			send_all(s, message, &len);
		}

		//If input is Publish
		else if (strcmp(input,"PUBLISH") == 0)
		{
			char message[1205];
			char files[1200];
			uint32_t count = 0;
			int16_t s_count = 0;

			DIR *directory = NULL;
			struct dirent *dir = NULL;

			//Directory doesn't exist
			if ((directory = opendir("SharedFiles")) == NULL)
			{
				printf("Unable to open directory\n");
				return 0;
			}
			//Reads through the directory
			while ((dir = readdir(directory)))
			{
				//If file is a normal type
				if (dir->d_type == DT_REG)
				{
					memcpy(files+s_count, dir->d_name, strlen(dir->d_name));
					s_count += strlen(dir->d_name);
					files[s_count] = 0;
					++s_count; ++count;
				}
			}
			closedir(directory);

			int size = 0;
			uint32_t count_nbo = htonl(count);

			//Puts all data into message
			message[0] = 1;
			size += 1;
			memcpy(message+size, &count_nbo, sizeof(count_nbo));
			size += sizeof(count_nbo);
			memcpy(message+size, files, s_count);
			size += s_count;

			//Sends Publish request to server
			send_all(s, message, &size);
		}

		//If input is Search
		else if (strcmp(input, "SEARCH") == 0)
		{
			std::string s_input;
			uint32_t ID; uint32_t addr; uint16_t port;

			//Receive input from user
			printf("Enter a file name: ");
			std::cin >> s_input;

			char message[2 + s_input.size()];
			message[0] = 2;
			memcpy(&message[1], s_input.data(), s_input.size()+1);
			char response[10];

			//Sends Search message to server
			int len = sizeof(message);
			if (send_all(s, message, &len) < 0) { return 1; }

			//Receive data back from server
			len = 10;
			receive_chunk(s, response, &len);

			//Copy data into response
			memcpy(&ID, &response[0], 4);
			memcpy(&addr, &response[4], 4);
			memcpy(&port, &response[8], 2);

			//If file is found
			if (addr != 0)
			{
				//Converts ip address
				char address[INET_ADDRSTRLEN];
				inet_ntop(AF_INET, &addr, address, sizeof(address));

				//Prints out file location
				printf("File found at\n");
				printf(" Peer %u\n", ntohl(ID));
				printf(" %s :",address);
				printf("%d\n", ntohs(port));
			}
			else //If file is not found
			{
    			printf("File not found\n");
    		}
		}

		else if (strcmp(input, "FETCH") == 0)
		{
			//Initialize Fetch and Search variables
			int fetch_s = 0;
			uint32_t ID; uint32_t addr; uint16_t port; 
			std::string s_input;
			char response[10];
			char f_data[1000];

			//Receive input from user
			std::cout << "Enter a file name: ";
			std::cin >> s_input; 

			//Initialize message
			char message[2 + s_input.size()];
			message[0] = 2;
			memcpy(&message[1], s_input.data(), s_input.size()+1);

			//Sends Search message to server
			int len = sizeof(message);
			if (send_all(s, message, &len) < 0) { return 1; }

			//Receive data from Search request
			len = sizeof(response);
			receive_chunk(s, response, &len);
			memcpy(&ID, &response[0], 4);
			memcpy(&addr, &response[4], 4);
			memcpy(&port, &response[8], 2);

			//If file is found
			if (addr != 0)
			{
				//Convert address to readable form
				char address[INET_ADDRSTRLEN];
				inet_ntop(AF_INET, &addr, address, sizeof(address));

				//Convert port to readable form
				port = ntohs(port);
				char f_port[10];
				sprintf(f_port, "%d", port);

				//Connect to correct peer
				if ((fetch_s = lookup_and_connect(address, f_port)) < 0) { return 1; }

				//Initialize Fetch message
				char fmessage[2 + s_input.size()];
				fmessage[0] = 3;
				memcpy(&fmessage[1], s_input.data(), s_input.size()+1);
				len = sizeof(fmessage);

				//Sends Fetch message
				if (send_all(fetch_s, fmessage, &len) < 0) { return 1; }

				//Initialize variables for opening file
				char file[s_input.size()];
				strcpy(file, s_input.c_str());
				int bytes_recv = 0;

				//Open file 
  				int f_open = open(file, O_WRONLY|O_CREAT|O_TRUNC, S_IRUSR|S_IWUSR);
  				if (!f_open) { std::cout << "Error: Couldn't open file"; return 1; }

				
			    //Write file data into file
			    recv(fetch_s, f_data, 1, 0);
				while ((bytes_recv = recv(fetch_s, f_data, sizeof(f_data), 0)) > 0)
				{
					write(f_open, f_data, bytes_recv);
				}

				//Close Fetch socket and file reader
				close(f_open);
				close(fetch_s);
			}
			else //If file is not found
			{
				printf("File not found\n");
			}
		}

		//If input is Exit 
		else if (strcmp(input, "EXIT") == 0)
		{
			connected = false;
			close(s);
		}

		//default case
		else
		{
			printf("Invalid Input\n");
		}
	}

	return 0;
}

//Given function in Lab 1
int lookup_and_connect( const char *host, const char *service ) {
	struct addrinfo hints;
	struct addrinfo *rp, *result;
	int s;

	/* Translate host name into peer's IP address */
	memset( &hints, 0, sizeof( hints ) );
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_flags = 0;
	hints.ai_protocol = 0;

	if ( ( s = getaddrinfo( host, service, &hints, &result ) ) != 0 ) {
		fprintf( stderr, "stream-talk-client: getaddrinfo: %s\n", gai_strerror( s ) );
		return -1;
	}

	/* Iterate through the address list and try to connect */
	for ( rp = result; rp != NULL; rp = rp->ai_next ) {
		if ( ( s = socket( rp->ai_family, rp->ai_socktype, rp->ai_protocol ) ) == -1 ) {
			continue;
		}

		if ( connect( s, rp->ai_addr, rp->ai_addrlen ) != -1 ) {
			break;
		}

		close( s );
	}
	if ( rp == NULL ) {
		perror( "stream-talk-client: connect" );
		return -1;
	}
	freeaddrinfo( result );

	return s;
}