import socket
import re

#sends SYN packet to server
def sendSYNpacket(seq):
    seq = str(seq)
    message = "Type:A,Seq:"+seq+",Syn:1,Ack:0"
    print("1st step of 3 way handshake")
    print("Client sends:", message)
    client.send(message.encode())

#sends ACK packet to server
def sendACKpacket(seq,serverseq):
    seq = str(seq)
    ack = str(serverseq + 1)
    message = "Type:A,Seq:"+seq+",Syn:0,Ack:"+ack
    print("3rd step of 3 way handshake")
    print("Client sends:", message)
    client.send(message.encode())

#Error cases
def errorMessage(errno):
    if(errno == 1):
        message = "Type:E, Timeout error, failed to connect."
    elif(errno == 2):
        message = "Type:E, Server failed to send proper packet, failed to connect."
    elif(errno == 3):
        message = "Type:E, Server failed to acknowledge client or missing vital information, failed to connect."
    elif(errno == 4):
        message = "Type:E, Client failed to send proper packet, failed to connect."
    elif(errno == 5):
        message = "Type:E, Client failed to acknowledge server or missing vital information, failed to connect."
    client.send(message.encode())
    print(message)
    client.close()

packtypeA_re = r'Type:A'
packtypeB_re = r'Type:B'
packtypeD_re = r'Type:D'
packtypeE_re = r'Type:E'
seq_re = r'Seq:[0-9]+'
syn_re = r'Syn:[0-9]+'
ack_re = r'Ack:[0-9]+'
seq = 100
host = "146.95.20.38"
port = 60495
BUFFER = 1024
error = -1
#create socket
client = socket.socket()
print("Client socket created")
#connect to server
client.connect((host, port))
print("Connection in progress...")
#send SYN packet and update sequence number
sendSYNpacket(seq)
seq += 1

servermessage = client.recv(BUFFER).decode()
print("Server sent:", servermessage)

typeA = re.findall(packtypeA_re, servermessage)
serverseq = re.findall(seq_re, servermessage)
serversyn = re.findall(syn_re, servermessage)
serverack = re.findall(ack_re, servermessage)

if(typeA == []):
    errorMessage(2)
    quit()
elif(serverseq == [] or serversyn == [] or serverack == []):
    errorMessage(3)
    quit()
    

typeA = ''.join(typeA)
serverseq = ''.join(serverseq)
serverseq = serverseq[4:]
serverseq = int(serverseq)
        
serversyn = ''.join(serversyn)
serversyn = serversyn[4:]
serversyn = int(serversyn)
        
serverack = ''.join(serverack)
serverack = serverack[4:]
serverack = int(serverack)

if(serversyn != 1 or serverack != seq):
    
    errorMessage(3)
    quit()

sendACKpacket(seq, serverseq)
seq += 1

servermessage = client.recv(BUFFER).decode()
typeD = re.findall(packtypeD_re, servermessage)
typeE = re.findall(packtypeE_re, servermessage)
print(servermessage)

if(typeE != []):
    client.close()
    quit()

message = "abc"
while(message != "Q"):
    message = input("Enter message: ")
    print(message)
    clientmessage = "Type:C,"+message
    client.send(clientmessage.encode())

client.close()
quit()

