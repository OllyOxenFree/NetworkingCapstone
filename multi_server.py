import socket
import os
import sys
import time

HOST = "192.168.1.11"
PORT = 8590
BUFFER = 1024
s = socket.socket()
s.bind((HOST,PORT))
s.listen(10)

childrenInAction = []
def reapChildren():
    while childrenInAction:
        pid, stat = os.waitpid(0, os.WNOHANG)
        if not pid:
            break
        childrenInAction.remove(pid)

#def transmitMessage(message)

def handleClient(connection):
    time.sleep(10)
    while True:
        message = connection.recv(BUFFER)
        if(not message):
            break
        broadcast = "Echo=>%s at %s" % (message, time.ctime(time.time()))
        connection.send(broadcast.encode())
    connection.close()
    os._exit(0)

def transmitter():
    while True:
        print("Server is actively listening for clients")
        client, address = s.accept()
        print("Server connection established at", address, "at", time.ctime(time.time()))
        reapChildren()
        childPid = os.fork()
        if childPid == 0:
            handleClient(connection)
        else:
            childrenInAction.append(childPid)

transmitter()
s.close()
