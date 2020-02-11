import socket 
import json  
import os                # Import socket module
from os import path
from Crypto.Cipher import DES3
from Crypto import Random

port = 60009                  # Reserve a port for your service.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             # Create a socket object
host = socket.gethostname()     # Get local machine name
s.bind(('127.0.0.1', port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print('Server listening....')

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

clientPubKeys = []

################################ opcode 10 ################################
def pubkey():
    # return prime,gen,pub
    # write definition here
    return 22147, 5, 2321 


################################ opcode 10 ################################

################################ DES3 Init ################################
def make_des3_encryptor(key, iv):
    encryptor = DES3.new(key, DES3.MODE_CBC, iv)
    return encryptor


def des3_encrypt(encryptor, data):
    pad_len = 8 - len(data) % 8 # length of padding
    padding = chr(pad_len) * pad_len # PKCS5 padding content
    data += padding
    return encryptor.encrypt(data)


def des3_decrypt(key, iv, data):
    encryptor = _make_des3_encryptor(key, iv)
    result = encryptor.decrypt(data)
    pad_len = ord(result[-1])
    result = result[:-pad_len]
    return result
iv = '00000000'
########## 24 Byte key ##########
key = 'dkdbhuer54poklnh67v53c7h' 
########## 24 Byte key ##########
des3 = make_des3_encryptor(key, iv)
################################ DES3 Init ################################

while True:
    conn, addr = s.accept()     # Establish connection with client.
    print('Got connection from', addr)
    data = conn.recv(1024).decode('utf-8')
    print('Server received', repr(data))
    parsed_json = (json.loads(data))
    print('Parsed Json: ',parsed_json)
    if 10 == parsed_json["header"]["opcode"]:
        clientPubKeys = parsed_json["publicKey"]
        clientKeyFilename = parsed_json["header"]["saddr"] + "-client.keys"
        with open(clientKeyFilename, 'w') as outfile:
            json.dump(clientPubKeys, outfile)
        prime1,gen1,pub1 = pubkey()
        prime2,gen2,pub2 = pubkey()
        prime3,gen3,pub3 = pubkey()
        Msg["header"]["opcode"] = 10
        Msg["header"]["saddr"] = host
        Msg["publicKey"]["id"] += 1
        Msg["publicKey"]["prime"] = [prime1, prime2, prime3]
        Msg["publicKey"]["gen"] = [gen1, gen2, gen3]
        Msg["publicKey"]["pub"] = [pub1, pub2, pub3]
        data_byte = bytes(json.dumps(Msg),'utf-8')
        conn.send(data_byte)
    if 20 == parsed_json["header"]["opcode"]:
        filename=parsed_json["request"]["filename"]
        f = open(filename,'rb')
        l = f.read(1024)
        while (l):
           conn.send(l)
           #print('Sent ',repr(l))
           l = f.read(1024)
        f.close()
    if 40 == parsed_json["header"]["opcode"]:
        clientKeyFilename = parsed_json["header"]["saddr"] + "-client.keys"
        fileExists = path.exists(clientKeyFilename)
        if fileExists:
            os.remove(clientKeyFilename)
        print("Resources of "+parsed_json["header"]["saddr"]+" are now expired.")
        Msg["header"]["opcode"] = 50
        data_byte = bytes(json.dumps(Msg),'utf-8')
        conn.send(data_byte)

    print('Done sending')
    #conn.send(b'Thank you for connecting')
    conn.close()
