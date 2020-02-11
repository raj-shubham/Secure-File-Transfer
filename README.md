# Secure-File-Transfer
Secure file transfer through 3-DES and Diffie-Hellman Key Exchange in Python

Please change the filenames to request that is hardcoded in client.py at line 225 and 235 

Step1:
python3 server.py
 
step2: 
python3 client.py PUBKEY
This step exchanges the shared values to generate the secret key using diffie hellman

step3:
python3 client.py REQSERV
This asks server for file transfer. The name of file is hardcoded in client.py

step:
python3 client.py REQCOM
This informs the server that the file is correctly received. From here, server deletes the keys it has saved for the sender.
On server's response, client does the same
