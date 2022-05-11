import socket
import sys

HOST = "192.168.1.11"
PORT = 8590
BUFFER = 1024

message = [b'All set!']

client = socket.socket()
client.connect((HOST,PORT))

for line in message:
    client.send(line)
    data = client.recv(BUFFER)
    print("Client received:", data)

client.close()
