import socket
import re


def sendSYNACKpacket(seq,clientseq):
    seq = str(seq)
    ack = str(clientseq + 1)
    message = "Type:A,Seq:"+seq+",Syn:1,Ack:"+ack
    print("2nd step of 3 way handshake")
    print("Server sends:", message)
    c.send(message.encode())

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
    c.send(message.encode())
    print(message)
    c.close()



packtypeA_re = r'Type:A'
packtypeB_re = r'Type:B'
packtypeD_re = r'Type:D'
packtypeE_re = r'Type:E'
seq_re = r'Seq:[0-9]+'
syn_re = r'Syn:[0-9]+'
ack_re = r'Ack:[0-9]+'

HOST = "146.95.20.38"
PORT = 60495
BUFFER = 1024
error = -1
success = 1
seq = 400
server = socket.socket()
print("Socket created successfully!")
server.bind((HOST,PORT))
print("Socket binded successfully!")

server.listen()
print("Socket is listening for potential connections...")
while True:
    #accept connection to start 3-Way handshake
    c, addr = server.accept()
    c.settimeout(10)
    print("Connection in progress...")

    #receive SYN packet from client
    clientmessage = c.recv(BUFFER).decode()
    #give error message if packet is not received before timeout
    if(not clientmessage):
        errorMessage(1)
        break
    print("Client sent", clientmessage)
    #find different segments of packet
    typeA = re.findall(packtypeA_re, clientmessage)
    clientseq = re.findall(seq_re, clientmessage)
    clientsyn = re.findall(syn_re, clientmessage)
    clientack = re.findall(ack_re, clientmessage)

    #error message if client fails to send proper packet
    if(typeA == []):
        errorMessage(4)
        break
    #error message if client doesn't include all segments of packet
    elif(clientseq == [] or clientsyn == [] or clientack == []):
        errorMessage(5)
        break

    #grab values of client SEQ and SYN number
    typeA = ''.join(typeA)
    clientseq = ''.join(clientseq)
    clientseq = clientseq[4:]
    clientseq = int(clientseq)
    clientsyn = ''.join(clientsyn)
    clientsyn = clientsyn[4:]
    clientsyn = int(clientsyn)

    #if client does not set SYN to 1, it does not wish to connect
    if(clientsyn != 1):
        errorMessage(5)
        break
    clientack = ''.join(clientack)
    clientack = clientack[4:]
    clientack = int(clientack)
    #send SYNACK packet using server and client SEQ number
    sendSYNACKpacket(seq, clientseq)
    seq += 1

    #receive ACK packet from client
    clientmessage = c.recv(BUFFER).decode()

    
    print("Client sent", clientmessage)
    typeE = re.findall(packtypeE_re, clientmessage)
    if(typeE != []):
        print("Connection failed.")
        c.close()
        break  
    typeA = re.findall(packtypeA_re, clientmessage)
    clientseq = re.findall(seq_re, clientmessage)
    clientsyn = re.findall(syn_re, clientmessage)
    clientack = re.findall(ack_re, clientmessage)


    if(typeA == []):
        errorMessage(4)
        break
    elif(clientseq == [] or clientsyn == [] or clientack == []):
        errorMessage(5)
        break
    typeA = ''.join(typeA)
    clientseq = ''.join(clientseq)
    clientseq = clientseq[4:]
    clientseq = int(clientseq)
        
    clientsyn = ''.join(clientsyn)
    clientsyn = clientsyn[4:]
    clientsyn = int(clientsyn)
        
    clientack = ''.join(clientack)
    clientack = clientack[4:]
    clientack = int(clientack)
    #if client's SYN is not 0 or client does not send proper ACK, send error message
    if(clientsyn != 0 or clientack != seq):
        errorMessage(5)
        break

    print("Connection established.")
    print("3 Way Handshake complete.")
    c.send("Type:D,Connection established.".encode())
    seq += 1
    message = ""
    c.settimeout(50)
    while(message != "Q"):
        clientmessage = c.recv(BUFFER).decode()
        message = clientmessage[7:]
        print(message)
    c.close()
    break
server.close()
