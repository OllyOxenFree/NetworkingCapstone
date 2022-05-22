import socket
import time
import sys
import queue
import select

HOST = "192.168.1.4"
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
"""
def broadcast(sock, msg):
    for s in readList:
        if s != main_sock and s != sock:
            try:
                s.send(msg)
            except:
                s.close()
                readList.remove(s)
                if s in writeList:
                    writeList.remove(s)
            else:
                print("Broadcast successful")
"""
while 1:
    reads, writes, errors = select.select(readList, writeList, errorList)
    for sock in reads:
        if sock == main_sock:
            connection, addr = sock.accept()
            connection.setblocking(1)
            print("New client from %s:%d" %addr)
            readList.append(connection)
            msg_queue[connection] = queue.Queue()
        else:
            try:
                data = sock.recv(BUFFER)
            except:
                print("Connection from", addr, "has been lost.")
                readList.remove(sock)
                if sock in writeList:
                    writeList.remove(sock)
                    sock.close()
                    del msg_queue[sock]
            else:
                if data:
                    print("Received data from", addr, ":", data)
                    msg_queue[sock].put(data)
                    if sock not in writeList:
                        writeList.append(sock)
            """
            else:
                if sock in writeList:
                    writeList.remove(sock)
                readList.remove(sock)
                sock.close()
                del msg_queue[sock]
            """
    for sock in writes:
        try:
            next_msg = msg_queue[sock].get_nowait()
        except queue.Empty:
            writeList.remove(sock)
        else:
            sock.send(next_msg)
    for sock in errors:
        if sock in readList:
            readList.remove(sock)
        if sock in writeList:
            writeList.remove(sock)
        if sock in errorList:
            errorList.remove(sock)
        sock.close()

        del msg_queue[sock]
