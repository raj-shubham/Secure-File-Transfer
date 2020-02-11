import socket                   # Import socket module
import json
import sys
import os
from os import path

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             # Create a socket object
host = socket.gethostname()     # Get local machine name
IPAddr = socket.gethostbyname(host)
port = 60009                    # Reserve a port for your service.
print(IPAddr)
state = 10
s.connect(('127.0.0.1', port))

serverFileName = 'server.keys'
# Send DH values

Hdr = {
	"opcode":None,  
	"saddr": None, 
	"daddr": None 
} 

PubKey = {
	"id":0,
	"prime": None, 
	"gen": None, 
	"pub": None 
} 

ReqServ = {
	"filename": None
}


Msg = {
	"header": Hdr,
	"publicKey": PubKey,
	"request": ReqServ,
	"ReqCom": False,
	"Disconnect": False
}

serverPubKeys = None

opcode = {
	"PUBKEY": 10,
	"REQSERV": 20,
	"ENCMSG": 30,
	"REQCOM": 40,
	"DISCONNET": 50
}

def pubkey():
	# return prime,gen,pub
	# write definition here
	return 242147, 2, 2321 

opcode_val = opcode[sys.argv[1]]
################################ opcode 10 ################################

if opcode_val == opcode["PUBKEY"]:
	prime1,gen1,pub1 = pubkey()
	prime2,gen2,pub2 = pubkey()
	prime3,gen3,pub3 = pubkey()
	Msg["header"]["opcode"] = 10
	Msg["header"]["saddr"] = IPAddr
	Msg["publicKey"]["id"] += 1
	Msg["publicKey"]["prime"] = [prime1, prime2, prime3]
	Msg["publicKey"]["gen"] = [gen1, gen2, gen3]
	Msg["publicKey"]["pub"] = [pub1, pub2, pub3]
	
	data_byte = bytes(json.dumps(Msg),'utf-8')
	s.send(data_byte)
	
	data = s.recv(1024).decode('utf-8')
	parsed_json = (json.loads(data))
	
	if 10 == parsed_json["header"]["opcode"]:
		serverPubKeys = parsed_json["publicKey"]
	print(serverPubKeys)
	with open(serverFileName, 'w') as outfile:
	    json.dump(serverPubKeys, outfile)
################################ opcode 10 ################################

################################ opcode 20 ################################

if opcode_val == opcode["REQSERV"]:
	Msg["header"]["opcode"] = 20
	Msg["header"]["saddr"] = IPAddr
	Msg["request"]["filename"] = "a.pdf"
	
	data_byte = bytes(json.dumps(Msg),'utf-8')
	s.send(data_byte)
	
	with open('received.pdf', 'wb') as f:
		print('file opened')
		while True:
			print('receiving data...')
			data = s.recv(1024)
			print('data=%s', (data))
			if not data:
				break
			# write data to a file
			f.write(data)
	f.close()
	print('Successfully get the file')
	s.close()
	print('connection closed')
	Msg["header"]["opcode"] = 30
################################ opcode 20 ################################

################################ opcode 40 ################################

if opcode_val == opcode["REQCOM"]:
	Msg["header"]["opcode"] = 40
	Msg["header"]["saddr"] = IPAddr
	
	data_byte = bytes(json.dumps(Msg),'utf-8')
	s.send(data_byte)
	
	data = s.recv(1024).decode('utf-8')
	parsed_json = (json.loads(data))
	if 50 == parsed_json["header"]["opcode"]:
		Msg["header"]["opcode"] = 50
		fileExists = path.exists(serverFileName)
		if fileExists:
			os.remove(serverFileName)
		print("Resources of the server are now expired.")
################################ opcode 20 ################################