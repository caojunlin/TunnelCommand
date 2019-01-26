from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from threading import Thread
import sys

class CommanderConnection(Thread):
    commanderConnection: socket

    def __init__(self, server, HOST_TCP, buffSize=1024):
        super().__init__()
        self.HOST_TCP = HOST_TCP
        self.server = server
        self.buffSize = buffSize
        self.waitForConnection()

    def waitForConnection(self):
        print("Waiting for commander connetion...\n")
        self.commanderConnection, addr = self.HOST_TCP.accept()
        print("Successfully accepted commander connection.\n")

    def run(self):
        while True:
            try:
                data = self.commanderConnection.recv(self.buffSize)
            except OSError:
                self.commanderConnection.close()
                print("Commander socket connection disconnected.")
                self.waitForConnection()
                print("Commander socket reconnected.")
                continue

            if not data:
                self.commanderConnection.close()
            else:
                try:
                    self.server.SlaverSession.targetConnection.send(data)
                except OSError:
                    pass


class SlaverConnection(Thread):
    targetConnection: socket

    def __init__(self, server, HOST_TCP, buffSize=1024):
        super().__init__()
        self.HOST_TCP = HOST_TCP
        self.server = server
        self.buffSize = buffSize
        self.waitForConnection()

    def waitForConnection(self):
        print("Waiting for target connetion...\n")
        self.targetConnection, addr = self.HOST_TCP.accept()
        print("Successfully accepted target connection.\n")

    def run(self):
        while True:
            try:
                data = self.targetConnection.recv(self.buffSize)
            except OSError:
                self.targetConnection.close()
                print("Commander socket connection disconnected.")
                self.waitForConnection()
                print("Commander socket reconnected.")
                continue

            if not data:
                self.targetConnection.close()
            else:
                try:
                    self.server.CommanderSession.commanderConnection.send(data)
                except OSError:
                    pass


class Server:
    def __init__(self):
        print("Working on server configuration ")
        self.HOST = self.getHostIP()
        self.POST = 11226
        self.ADDR = (self.HOST, self.POST)
        self.HOST_TCP = socket(AF_INET, SOCK_STREAM)
        self.HOST_TCP.bind(self.ADDR)
        self.HOST_TCP.listen(3)
        self.SlaverSession = SlaverConnection(self, self.HOST_TCP)
        self.SlaverSession.start()
        self.CommanderSession = CommanderConnection(self, self.HOST_TCP)
        self.CommanderSession.start()
        self.hold()

    def getHostIP(self):
        skt = socket(AF_INET, SOCK_DGRAM)
        skt.connect(("0.0.0.0", 80))
        return skt.getsockname()[0]

    def hold(self):
        while True:
            pass

if __name__ == '__main__':
    SV = Server()
