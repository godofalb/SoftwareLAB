# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:53:18 2019

@author: xwl99
"""
import os
import sys
import threading
import struct
import subprocess
from socket import *
from validation import *
import re
import inspect
import ctypes
from Encryption import * 

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 
 
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

class CServer:
    def __init__(self,host='127.0.0.1',port=8878,logF="DefaultServerLog.txt",inP=sys.stdin,outP=sys.stdout ):
        self.clients={}
        #self.encryption=Encryption("Test")
        self.validation=validation()
        self.pwdPattern=r"\[(.*?),(.*?)\](.*)"
        self.logFile=logF
        self.listenningSocket=socket(AF_INET,SOCK_STREAM)
        self.listenningSocket.bind((host,port))
        
        self.listeningThread=threading.Thread(target=self.waiting)
        
        self.InputThread=threading.Thread(target=self.winput)
        self.outStream=outP
        self.inStream=inP
    def Start(self):
        if os.path.exists(self.logFile):
            self.logFile=open(self.logFile,'a+')
        else:
            self.logFile=open(self.logFile,'w')
        self.outStream.write('StartTheServer\n')
        self.listenningSocket.listen(10)
        self.listeningThread.start()
        self.outStream.write('StartListenning\n')
        self.InputThread.start()
        self.outStream.write('Complete\n')
    def End(self):
        self.outStream.write('Exiting\n')
        self.logFile.close()
        for k in self.clients:
            if self.clients[k]:
                stop_thread(self.clients[k][0])
                stop_thread(self.clients[k][3])
        
        self.listeningThread.Thread_running=False
        self.listenningSocket.close()
        self.outStream.write('Exiting2\n')
        exit()
       # print( dir(self.listeningThread))
       # self.InputThread.terminate()
        
    def ExceteCMD(self,s,commandLine):
        '''
            Not used
        '''
        pass
    def EhowClients(self):
        s=''
        for k in self.clients:
            s+=str(k)+'\n'
        return s
    def responseCommandLine(self,s,cmd,addr):
        for line in iter(cmd.stdout.readline,b''):
            if cmd.poll() is None:
                s.send(line)
        sto,ste=cmd.communicate()
        s.send(sto)
        print('Exiting response')
        
    def commandLine(self,s,addr):
        self.clients[addr][2]=subprocess.Popen("cmd.exe",shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        newThread=threading.Thread(target=self.responseCommandLine,args=(s,self.clients[addr][2],addr))
        newThread.start()
        self.clients[addr][3]=newThread
        e=self.clients[addr][4]
        while 1:
            try:
                sentence=s.recv(2048)
                self.logging("Reced\n")
                
                if len(sentence)<1:
                    self.logging('收到过短的字符串 从%s\n'%(str(addr)))
                    self.outStream.write('收到过短的字符串 从%s\n'%(str(addr)))
                    break
                sentence=e.DecryptString(sentence)
                #sentence=self.encryption.DecryptString(sentence)
                #sentence=sentence.decode('gbk')
               # self.outStream.write("Reced %s\n"%sentence)
                i,sentence=self.validate(sentence)
                
                if i==-1:
                    self.outStream.write('密码错误 从%s\n'%(str(addr)))
                    s.send('stop'.encode('gbk'))
                    s.close()
                    break
                if not i==1:
                    continue
                if sentence=='stop':
                    self.outStream.write('收到停止请求 从%s\n'%(str(addr)))
                    s.send('stop'.encode('gbk'))
                    s.close()
                    break
               # print ('|'+sentence+'|')
                if sentence=='show':
                    self.outStream.write('收到显示请求\n')
                    w=self.EhowClients()
                    s.send(('目前连接:%s\n'%(str(w))).encode('gbk'))
                    continue
                self.clients[addr][2].stdin.write(sentence.encode('gbk'))
                self.clients[addr][2].stdin.write('\n'.encode('gbk'))
                self.clients[addr][2].stdin.flush()
                    #self.outStream.write("%s\n>"%(sentence))
                    #s.send('recvd'.encode('gbk'))
            except Exception as e:
                self.outStream.write(str(e)+"\n>")
                s.send('stop'.encode('gbk'))
                s.close()
                break
            finally:
                pass
        
        newThread.join(2)
        self.clients[addr][2].kill()
        #stop_thread(newThread)
        self.clients[addr]=None
        self.outStream.write("Close Connection"+str(addr)+"\n>")
        return
    def validate(self,cmd):
        m=re.match(self.pwdPattern,cmd)
       # print(m[1],m[2])
        if m:
            return self.validation.LoginCheck(m[1],m[2]),m[3]
        else:
            return -3,None
    def winput(self):
        while 1:
            self.outStream.write(">")
            a=self.inStream.readline()
            if a=='stop\n':
                self.End()
                
                return
            if a=='thread\n':
                s=len(threading.enumerate())
                self.outStream.write("线程数量%d\n>"%(s))
    def waiting(self):
        while 1:
            try:
                connectionSocket,addr=self.listenningSocket.accept()
                self.outStream.write("New connection:\n")
                self.outStream.write (str(addr)+"\n>")
                self.CreateNewClient(connectionSocket,addr)
            except Exception as e:
                if not str(e)=='[WinError 10038] 在一个非套接字上尝试了一个操作。':
                    self.outStream.write(str(e)+"\n")
                    self.logging(str(e)+"\n")
                return
    def CreateNewClient(self,connectionSocket,addr):
        usename=connectionSocket.recv(2048).decode('utf-8')
        en=Encryption(usename)
        pwd=connectionSocket.recv(2048)
        pwd=en.DecryptString(pwd)
        en.LoadKey(pwd)
        if self.validation.LoginCheck(usename,pwd)!=1:
            connectionSocket.close()
            return
       # print(usename,pwd)
        connectionSocket.send('OK'.encode('utf-8'))
        newThread=threading.Thread(target=self.commandLine,args=(connectionSocket,addr))
        self.clients[addr]=[newThread,connectionSocket,None,None,en]
        newThread.start()
    def logging(self,text):
        self.logFile.write(text)
    
if __name__=='__main__':
    CS=CServer()#host='10.27.68.32'
    CS.Start()
   # CS.logging('test')
   # CS.logging('test2')
    #CS.End()
'''
serverPort=44000
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print 'Ready'
while 1:
	connectionSocket,addr=serverSocket.accept()
	sentence=connectionSocket.recv(1024)
	print sentence,addr
	capitalizedSentence=sentence.upper()
	connectionSocket.send(capitalizedSentence)
	connectionSocket.close()
'''
