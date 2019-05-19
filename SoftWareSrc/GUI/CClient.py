# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:50:55 2019

@author: xwl99
"""
from socket import *
import struct
import time
import sys
import threading
import os
from Encryption import * 
import queue

class CClient(threading.Thread):
    def __init__(self, ginp_q=None, gout_q=None,host='127.0.0.1', port=8878, 
                logF="DefaultServerLog.txt",inP=sys.stdin, outP=sys.stdout, 
                pfile='Password.txt'):
        super(CClient, self).__init__()
        self.addr=(host,port)
        self.pfile=pfile
        self.currentLoginInfo=("","")
        self.loginInfos={}
        self.loadFile(pfile)
        self.encryption=Encryption(self.currentLoginInfo[1])
        self.logFile=logF
        self.socket=socket(AF_INET,SOCK_STREAM)
        self.socketConnected=False
        self.stoped=False
        self.outStream=outP
        self.inStream=inP
        self.inputThread=threading.Thread(target=self.winput)
        self.inputThread.start()
        #self.listenningSocket=socket(AF_INET,SOCK_STREAM)
        #self.listenningSocket.bind((host,port))
        #self.listenningSocket.listen(10)

        self.ginp_q = ginp_q
        self.gout_q = gout_q

    def loadFile(self,filename):
        if os.path.exists(filename):
          # print('L')
            f=open(filename,'r')
            
            for i in f.readlines():
                us=i[:-1].split(',')
                if len(us)==2:
                    usname=us[0]
                    pw=us[1]
                    self.loginInfos[usname]=(usname,pw)
                    self.setDefault(usname)
        
    def setDefault(self,name):
        if name in self.loginInfos.keys():
            self.currentLoginInfo=self.loginInfos[name]
            return True
        return False
    def addUser(self,name,pwd):
        if not (name in self.loginInfos.keys()):
            self.loginInfos[name]=(name,pwd)
            return True
        return False
    def addAndSet(self,name,pwd):
        if self.addUser(name,pwd):
            return self.setDefault(name)
        else:
            return False
    def Start(self):
        if os.path.exists(self.logFile):
            self.logFile=open(self.logFile,'a+')
        else:
            self.logFile=open(self.logFile,'w')
    def receive(self):
        while 1:
            try:
                callback=self.socket.recv(2048).decode('gbk')
                if callback=="stop":
                    self.End()
                    return
                # self.outStream.write("%s"%(callback))
                self.gout_q.put("%s"%(callback))
            except Exception as e:
                # self.outStream.write("%s\n"%("停止连接"))
                self.gout_q.put("%s\n"%("停止连接"))
                return
    def winput(self):
        # self.outStream.write("Welcome to use\ntype 'Help' for more informatiom\n")
        while not self.stoped:
            if not self.socketConnected:
                self.outStream.write(">")
                self.outStream.flush()
            # a=self.inStream.readline()
            a = self.ginp_q.get()
            # print('|'+a+'|')
            if a=='stop':
                self.End()
                return
            elif a=='CurrentUsers':
                # self.outStream.write('%s\n'%(str(self.loginInfos)))
                self.gout_q.put('%s\n'%(str(self.loginInfos)))
                continue
            elif a=='CurrentUser':
                # self.outStream.write('%s\n'%(str(self.currentLoginInfo)))
                self.gout_q.put('%s\n'%(str(self.currentLoginInfo)))
                continue
            elif a=='Set':
                # self.outStream.write('Input username\n>')
                self.gout_q.put('Input username\n>')
                # a2=self.inStream.readline()[:-1]
                a2 = self.ginp_q.get()
                if self.setDefault(a2):
                    # self.outStream.write('Success\n')
                    self.gout_q.put('Success\n')
                else:
                    # self.outStream.write('Error, incorrect user name\n')
                    self.gout_q.put('Error, incorrect user name\n')
            elif a=='AddAndSet':
                # self.outStream.write('Input username and password\n>')
                self.gout_q.put('Input username and password\n>')
                # a2=self.inStream.readline()[:-1]
                a2 = self.ginp_q.get()
                aa=a2.split(',')
                if len(aa)==2:
                    if self.addAndSet(aa[0],aa[1]):        
                        # self.outStream.write('Success\n')
                        self.gout_q.put('Success\n')
                    else:
                        # self.outStream.write('Error, might be multidefined\n')
                        self.gout_q.put('Error, might be multidefined\n')
                else:
                    # self.outStream.write('Error, format "username,password"\n')
                    self.gout_q.put('Error, format "username,password"\n')
            elif a=='Add':
                # self.outStream.write('Input username and password\n>')
                self.gout_q.put('Input username and password\n>')
                # a2=self.inStream.readline()[:-1]
                a2 = self.ginp_q.get()
                aa=a2.split(',')
                if len(aa)==2:
                    if self.addUser(aa[0],aa[1]):        
                        # self.outStream.write('Success\n')
                        self.gout_q.put('Success\n')
                    else:
                        # self.outStream.write('Error, might be multidefined\n')
                        self.gout_q.put('Error, might be multidefined\n')
                else:
                    # self.outStream.write('Error, format "username,password"\n')
                    self.gout_q.put('Error, format "username,password"\n')
            elif a=='Help':
#                 self.outStream.write('''
# local ins:
# Command      Usage
# Set          Set default user
# Add          Add new user
# AddAndSet    Add and set
# Connect      Use this user to login
# CurrentUsers Show the current user table, which is load from Password.txt
# CurrentUser  Show the curretn user

# Remote ins:
# Command      Usage
# stop         stop the connection
# show         show the current user on remote server
# Dos command  run in Remote

#                     ''')
                self.gout_q.put('''
local ins:
Command      Usage
Set          Set default user
Add          Add new user
AddAndSet    Add and set
Connect      Use this user to login
CurrentUsers Show the current user table, which is load from Password.txt
CurrentUser  Show the curretn user

Remote ins:
Command      Usage
stop         stop the connection
show         show the current user on remote server
Dos command  run in Remote

''')
               # print('Connecting')
                continue
            elif a=='Connect':
                # self.outStream.write('Connecting\n')
                self.gout_q.put('Connecting\n')
               # print('Connecting')
                self.CreateNewClient()
                self.encryption.LoadKey(self.currentLoginInfo[0])
                i1=self.encryption.EncryptSring(self.currentLoginInfo[1])
                self.socket.send(self.currentLoginInfo[0].encode('utf-8'))
                time.sleep(0.1)
                self.socket.send(i1)
                r=self.socket.recv(2048).decode('utf-8')
                if r=='OK':    
                    self.encryption.LoadKey(self.currentLoginInfo[1])
                    t=threading.Thread(target=self.receive)
                    t.start()
                    continue
                else:
                    self.logging("Error login")
                    # self.outStream.write("%s"%('Error login'))
                    self.gout_q.put("%s"%('Error login'))
                    return
            self.ExecuteCMD(a)
            #self.outStream.write("%s"%(r))
           # if r=="stop":
            #    self.End()
           #     return
           
    def End(self):
        self.logFile.close()
        # self.outStream.write("%s\n>"%("停止中。。。"))
        self.gout_q("%s\n>"%("停止中。。。"))
        r=self.ExecuteCMD('stop')
       # if r=='stop':
        if self.socketConnected:
            self.socket.close()
            self.socketConnected=False
        r=open(self.pfile,'w')
        for k in self.loginInfos:
            r.write('%s,%s\n'%(self.loginInfos[k][0],self.loginInfos[k][1]))
        r.close()
        self.stoped=True
    def ExecuteCMD(self,cmd):
        if self.socketConnected and cmd:
            cmd="["+self.currentLoginInfo[0]+","+self.currentLoginInfo[1]+"]"+cmd
            cd=self.encryption.EncryptSring(cmd)
           # cd=cmd.encode('gbk')
            self.socket.send(cd)
            time.sleep(0.1)
            #callback=self.socket.recv(2048).decode('gbk')
            #return callback
        return ""
    def CreateNewClient(self):
        self.socket.connect(self.addr)
        self.socketConnected=True
        
        # print('Connected\n>')
        self.gout_q.put('Connected\n>')
        '''
        a=input()
        a=a.encode('utf-8')
        print(len(a))
        p=struct.pack('i',len(a))
        self.socket.send(p+a)
        time.sleep(10)
        self.socket.close()'''
    def logging(self,text):
        self.logFile.write(text)

# if __name__=='__main__':
#     c=CClient()
#     c.Start()
#     #c.CreateNewClient()
#     '''

# serverName="127.0.0.1"
# serverPort=44000
# clientSocket=socket(AF_INET,SOCK_STREAM)
# clientSocket.bind(('',44001))
# print((serverName,serverPort))
# clientSocket.connect((serverName,serverPort))
# sentence=raw_input("Input lowcase sentence:")
# clientSocket.send(sentence)
# modifiedSentence=clientSocket.recv(1024)
# print 'From Server:',modifiedSentence
# clientSocket.close()
# '''