#-*-coding:utf-8 -*-
from socket import *
from threading import Thread
from time import  ctime
import os
import sys

class Server_file(object):                                                 #the file's transport of Server
    """docstring for Server_file"""
    def __init__(self):
        super(Server_file, self).__init__()

        self.BASE_DIR=os.path.dirname(os.path.abspath(__file__))
        self.path=None

        self.HOST='127.0.0.1'                                              #Server's address of IP
        self.PORT=2159                                                     #Server's port
        self.BUFSIZ=1024
        self.ADDR = (self.HOST,self.PORT)
        self.tcpCliSock = socket(AF_INET,SOCK_STREAM)                      #build the new socket object
        self.tcpCliSock.bind(self.ADDR)                                    #bind the IP
        self.socket_num=5
        self.tcpCliSock.listen(self.socket_num)
        self.conn=None
        self.addr=None
        self.socks=[]
        self.has_sent=0
        print('服务开启成功！\n')

    def connect_client(self):                                     
        print('服务器等待连接。。')                                           #The connection is blocked by self.tcpCliSock.accept()
        self.conn,self.addr=self.tcpCliSock.accept()
        print("{0},{1} 已连接！".format(self.addr[0],self.addr[1]))

    def upload_file_header(self):                                          #Collaborate with the client to create a file directory(/data/)
        try:
            while True:
                self.conn,self.addr=self.tcpCliSock.accept()
                print("{0},{1} 已连接！".format(self.addr[0],self.addr[1]))
                # self.conn.setblocking(0)
                self.socks.append(self.conn)
                while True:
                    for s in self.socks:
                        try:
                            data = self.conn.recv(self.BUFSIZ)     
                        except Exception as e:        
                            continue
                        cmd,self.file_name,file_size = str(data,'utf-8').split('|')
                        print(cmd,self.file_name,file_size)
                        self.path = os.path.join(self.BASE_DIR,'data')
                        if not os.path.exists(self.path):
                            os.mkdir(self.path)
                        self.path = os.path.join(self.path,self.file_name)
                        self.file_size = int(file_size)
    def upload_file_process(self):                                           #After the directory is created, prepare the transfer file
        if self.path!=None:
            with open(self.path,'wb') as fp:
                while self.has_sent != self.file_size:
                    data = self.conn.recv(self.BUFSIZ)
                    fp.write(data)
                    self.has_sent+=len(data)
                    print('\r'+'[保存进度]：%s%.02f%%' %('>'*int((self.has_sent/self.file_size)*50),float(self.has_sent/self.file_size)*100),end='')
            print('%s 保存成功！'%(self.file_name))
        else:
            print('please use upload_file_header to load file path')
            pass





class Client_file(object):                                                    #the file's transport of Client
    """docstring for client_file"""
    def __init__(self):
        super(Client_file, self).__init__()

        self.BASE_DIR=os.path.dirname(os.path.abspath(__file__))
        self.path=None

        self.has_sent=0
        self.file_size=0
        self.HOST='127.0.0.1'                                                 #Server's address of IP
        self.PORT=2159                                                        #Server's port
        self.BUFSIZ=1024
        self.ADDR = (self.HOST,self.PORT)

        self.tcpCliSock=None



    def connect_server(self):
        self.tcpCliSock = socket(AF_INET,SOCK_STREAM)                         #create the new Client's socket object
        self.tcpCliSock.connect(self.ADDR)                                    #connect the IP address

    def upload_file_header(self,cmd,content):                                 #
        self.path = os.path.join(self.BASE_DIR,content)
        self.file_name=os.path.basename(self.path)
        self.file_size=os.stat(self.path).st_size
        file_info = '%s|%s|%s' %(cmd,self.file_name,self.file_size)
        self.tcpCliSock.sendall(bytes(file_info,'utf-8'))
    def upload_file_process(self):
        if self.path != None:
            with open(self.path,'rb') as fp:
                self.tcpCliSock.recv(self.BUFSIZ)
                while self.has_sent != self.file_size:
                    data = fp.read(self.BUFSIZ)
                    self.tcpCliSock.send(data)
                    self.has_sent+=len(data)
                    print('\r'+'[保存进度]：%s%.02f%%' %('>'*int((self.has_sent/self.file_size)*50),float(self.has_sent/self.file_size)*100),end='')
                print('%s 保存成功！'%(self.file_name))

        else:
            print('please use load_file_header to load file path')
            pass

