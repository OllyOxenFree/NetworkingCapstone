import socket
import sys
import select

HOST = "192.168.1.4"
PORT = 7290
BUFFER = 1024

client = socket.socket()
client.connect((HOST, PORT))
client.setblocking(1)

while 1:
    """
    readList = [socket.socket(), client]
    reads, writes, errors = select.select(readList, [], [])

    for sock in reads:
        if sock == client:
            data = sock.recv(BUFFER)
            if data:
                print(data)
        else:
            msg = input("Enter message: ")
            sock.send(msg)
    """  
    message = input("Enter message: ")
    client.send(message.encode())
    data = client.recv(BUFFER)
    if data:
        print(data)
client.close()
