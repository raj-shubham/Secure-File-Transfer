/*
** client.c -- a stream socket client demo
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <stdio.h> 
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>

#include <arpa/inet.h>

#define PORT "3490" // the port client will be connecting to 

#define MAXDATASIZE 100 // max number of bytes we can get at once 

#define LENGTH 1024

struct Hdr{
	int opcode;
	//string saddr;
	//string daddr;
};

struct PubKey{
	long q;
	long a;
	long Y;
};

struct ReqServ{
	int opcode;
};

struct ReqCom{
	int opcode;
};

struct EncMsg{
	int message;
};

struct Disconnect{
	int opcode;
};

union commands{
	PubKey pubkey;
	ReqServ reqserv;
	ReqCom reqcom;
	EncMsg encmsg;
	Disconnect disconnect;
};

struct Msg{
	Hdr hdr; /* Header for a message */
	commands cmd;
};

// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
	if (sa->sa_family == AF_INET) {
		return &(((struct sockaddr_in*)sa)->sin_addr);
	}

	return &(((struct sockaddr_in6*)sa)->sin6_addr);
}



int main(int argc, char *argv[])
{
	int sockfd, numbytes;  
	char buf[MAXDATASIZE];
	char revbuf[LENGTH];
	struct addrinfo hints, *servinfo, *p;
	int rv;
	char s[INET6_ADDRSTRLEN];

	if (argc != 2) {
	    fprintf(stderr,"usage: client hostname\n");
	    exit(1);
	}

	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;

	if ((rv = getaddrinfo(argv[1], PORT, &hints, &servinfo)) != 0) {
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
		return 1;
	}

	// loop through all the results and connect to the first we can
	for(p = servinfo; p != NULL; p = p->ai_next) {
		if ((sockfd = socket(p->ai_family, p->ai_socktype,
				p->ai_protocol)) == -1) {
			perror("client: socket");
			continue;
		}

		if (connect(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
			perror("client: connect");
			close(sockfd);
			continue;
		}

		break;
	}

	if (p == NULL) {
		fprintf(stderr, "client: failed to connect\n");
		return 2;
	}

	inet_ntop(p->ai_family, get_in_addr((struct sockaddr *)p->ai_addr),
			s, sizeof s);
	printf("client: connecting to %s\n", s);

	freeaddrinfo(servinfo); // all done with this structure

	/*
	if ((numbytes = recv(sockfd, buf, MAXDATASIZE-1, 0)) == -1) {
	    perror("recv");
	    exit(1);
	}

	buf[numbytes] = '\0';
	Msg *incomingPtr;
	Msg incomingStr;
	incomingPtr = (struct Msg *)&buf;
	incomingStr = *incomingPtr;
	printf("client: received '%d'\n",incomingStr.cmd.encmsg.message);
	*/

	char* fr_name = "/Users/mymac/Desktop/Assignments/SNS-Assignments/Assignment1/Secure-File-Transfer/received.pdf";
	FILE *fp;
	int bytesReceived;
   	fp = fopen(fr_name, "ab");
   	if(NULL == fp)
   	{
   	    printf("Error opening file");
   	    return 1;
   	}

   	while((bytesReceived = read(sockfd, revbuf, LENGTH)) > 0)
    {
        printf("Bytes received %d\n",bytesReceived);    
        // recvBuff[n] = 0;
        fwrite(revbuf, 1,bytesReceived,fp);
        // printf("%s \n", recvBuff);
    }

    if(bytesReceived < 0)
    {
        printf("\n Read Error \n");
    }


	close(sockfd);

	return 0;
}
