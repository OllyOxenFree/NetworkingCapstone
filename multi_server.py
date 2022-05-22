import socket
import time
import sys
import queue
import select

HOST = "192.168.1.8"
PORT = 7290
BUFFER = 1024
main_sock = socket.socket()
print("Socket created")
main_sock.bind((HOST,PORT))
print("Socket binded")
main_sock.listen(5)
print("Waiting for connection...")

readList = [main_sock]
writeList = []
errorList = []
msg_queue = {}


while 1:
    reads, writes, errors = select.select(readList, writeList, errorList)
    for sock in reads:
        if sock == main_sock:
            connection, addr = sock.accept()
            connection.setblocking(1)
            print("New client from %s:%d" %addr)
            connection.setblocking(0)
            readList.append(connection)
            msg_queue[connection] = queue.Queue()
        else:
            data = sock.recv(BUFFER)
            if data:
                print("Received data")
                msg_queue[sock].put(data)
                if sock not in writeList:
                    writeList.append(sock)
            else:
                if sock in writeList:
                    writeList.remove(sock)
                readList.remove(sock)
                sock.close()
                del msg_queue[sock]

    for sock in writes:
        try:
            next_msg = msg_queue[sock].get_nowait()
        except queue.Empty:
            writeList.remove(sock)
        else:
            sock.send(next_msg.encode())

    for sock in errors:
        if sock in readList:
            readList.remove(sock)
        if sock in writeList:
            writeList.remove(sock)
        if sock in errorList:
            errorList.remove(sock)
        sock.close()

        del msg_queue[sock]
