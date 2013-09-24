#! usr/bin/python3
# DESC: 
#   currently, it is an command line interface
#
# TODO:
#
#   page up 224 73
#   page down 224 81



import socket
import sys
from threading import Thread
import msvcrt
import time
from multiConsole import *
import pickle


class bufferPresenter:
    '''
        this class is a abstract for the way of text present
        now, there are two way.
        1. cmd
        2. gui
    ''' 
    def showMsg(self, msg):
        raise NoImplementedError

    def sendMsg(self):
        raise NoImplementedError 
        # this will be triggerd when the subclass doesn't implement it, use the name to judge, if the arguement
        # is not the same is ok


class cmdPresenter(bufferPresenter):
    '''
        auto decode and encode 
    '''
    def __init__(self):
        self.panel = {} # contain each widget

        self.hstdout = dll.Kernel32.GetStdHandle(DWORD(-11))

        if(self.hstdout == HANDLE(-1)):
            print('create buffer failed')


        self.backBuffer = consoleBackBuffer(80, 18)

        self.panel['userpanel'] = usermenu(56, 0, 15, 17)
        self.panel['chatroom'] = msgroom(0, 0, 55, 17)
        self.panel['inLabel'] = inputLabel(0, 18, 71, 3)

        self.panel['userpanel'].title = 'user list'
        self.panel['chatroom'].title = 'chat room'

        self.backBuffer.gotoxy(1, 19, self.hstdout) # the cursor pos for input

        self.updateList = []
        self.updateList.append(self.panel['userpanel'])
        self.updateList.append(self.panel['chatroom'])
        self.updateList.append(self.panel['inLabel'])

        for panel in self.panel.values():
            panel.update()

        self.display()

    def getPanel(self):
        return self.panel

    def getUserAndMsg(self):
        return (self.panel['userpanel'].getContent(), self.panel['chatroom'].getContent())

    def setUserAndMsg(self, data):
        self.panel['userpanel'].setContent(data[0])
        self.panel['chatroom'].setContent(data[1])
        self.panel['userpanel'].update()
        self.panel['chatroom'].update()


    def getKeypress(self):
        '''
            it seems that this has a conflict with the input() function
        '''
        while True:
            if msvcrt.kbhit():
                key = ord(msvcrt.getch())
                if key == 224:
                    key = ord(msvcrt.getch())
                    if key == 73: # pageup
                        self.panel['chatroom'].scrollContent(-2)
                    elif key == 81:
                        self.panel['chatroom'].scrollContent(2)
                
            return input()
        # def clearInput():
        #   self.backBuffer.gotoxy(1, 19, self.hstdout)
        #   print(' '*70)
        
        # result = {32: clearInput }.get(key, lambda : None)
        # default will do nothing!!!
        # 32 -- the enter key
            


    def display(self):
        for p in self.updateList:
            if p == self.panel['inLabel']:
                p.display(self.hstdout)
                self.updateList.remove(self.panel['inLabel'])
            else:
                p.update()
                p.display(self.backBuffer.getHandle())


        self.backBuffer.present(self.hstdout)
        
    def showMsg(self, msg):
        ''' use print '''
        self.panel['chatroom'].addContent(msg)
        self.panel['chatroom'].update()
        
    def sendMsg(self):
        ''' use input(), after press enter will send the msg and clear the input region '''
        msg = input()
        self.panel['chatroom'].scroll = 0
        self.backBuffer.gotoxy(1, 19, self.hstdout) # the cursor pos for input
        self.updateList.append(self.panel['inLabel'])
        return msg


class guiPresenter(bufferPresenter):
    '''
    '''
    def __init__(self):
        pass






class baseSocket:
    '''
        create a prototype for server and client?
        ex  prototype   -- { create socket, __enter__, __exit__ }
              /    \
             /      \
        server     client
    '''
    def __init__(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print('failed to create socket. error code:{}'.format(e))
            sys.exit()


    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        print('socket close..')
        self.socket.close()


class server(baseSocket):
    '''
        no matter server or client, all things about Internet need a socket
        AF -- address family
        socket.socket(family, type,..)

        step:
        1. create socket
        2. bind a server
        3. listen
        4. recv/send

        note: use with xxx as xx syntax

        now put the cmd process here, and send the cmd object by pickle
        and client can get the cmd object and than call display()
    '''
    def __init__(self):
        super().__init__()
        
        self.panel = None

        self.host = socket.gethostbyname(socket.gethostname())#a windows way to get ip address
        self.port = 8888
        print('your ip:{} and port:{}'.format(self.host, self.port))

        try:
            self.socket.bind((self.host, self.port))
        except:
            print('bind failed')
            sys.exit()

        self.connAndAddr = []
        self.socket.listen(5)

    def getIPandPort(self):
        return (self.host, self.port) # a tuple str and int

    def start(self):
        while True:

            conn, addr = self.socket.accept()
            #print('connecting with {}:{}'.format(addr[0], addr[1]))

            username = conn.recv(4096).decode('utf-8')
            self.connAndAddr.append((conn, addr, username))
            panel = conn.recv(4096)

            if self.panel == None:
                self.panel = pickle.loads(panel)
            self.panel['userpanel'].addContent(username)


            #conn.sendall(pickle.dumps(self.panel['userpanel'].getContent()))

            t = Thread(target=self.process, args=(conn,))
            t.start()

            t2 = Thread(target=self.sendUserAndMsg)
            t2.start()

    def sendUserAndMsg(self):
        while True:
            for obj in self.connAndAddr:
                obj[0].sendall(pickle.dumps((self.panel['userpanel'].getContent(), self.panel['chatroom'].getContent())))
            time.sleep(0.05)


    def process(self, conn):
        while True:
            try:
                data = conn.recv(4096)
            except:
                print('error or client closed')
                for i in range(len(self.connAndAddr)):
                    if conn in self.connAndAddr[i]:
                        self.panel['userpanel'].delContent(self.connAndAddr[i][2])
                        self.panel['chatroom'].addContent(self.connAndAddr[i][2]+' leave...')
                        self.connAndAddr.pop(i)
                        break

                conn.close()
                break

            self.panel['chatroom'].addContent(data.decode('utf-8'))

            # for obj in self.connAndAddr:
            #   obj[0].sendall(pickle.dumps(self.panel['chatroom'].getContent()))
        conn.close()



class client(baseSocket):
    '''
        step:
        1. create socket
        2. connect
        3. recv/send
    
    '''
    def __init__(self, host, port):
        super().__init__()
        self.name = ''

        try:
            self.socket.connect((host, port))
        except:
            print('server is not open')

        self.presenter = cmdPresenter()
        self.presenter.display()


    def display(self):
        while True:
            data = pickle.loads(self.socket.recv(4096))
            self.presenter.setUserAndMsg(data)
            self.presenter.display()
            time.sleep(0.05)


    def setUserName(self, name):
        self.name = name


    def start(self):
        self.socket.sendall(self.name.encode('utf-8'))
        self.socket.sendall(pickle.dumps(self.presenter.getPanel()))

        userlist = pickle.loads(self.socket.recv(4096))
        

        t = Thread(target=self.display)
        t.start()
        while True:
                msg = self.name+': '+self.presenter.sendMsg()
                msg = msg.encode('utf-8')
                self.socket.sendall(msg)



def test():
    name = input('enter your name: ')

    if input('enter 1p or 2p').upper() == '1P':
        # means server
        with server() as s:
            print('press any key to continue')
            msvcrt.getch()
            t = Thread(target=s.start)
            t.start()


            host, port = s.getIPandPort()
            
            with client(host, port) as c:
                c.setUserName(name)
                c.start()
    else:

        host = '124.9.33.117'
        port = 8888

        with client(host, port) as c:
            c.setUserName(name)
            c.start()


if __name__ == '__main__':  
    #test()
    name = input('enter your name: ')

    if input('enter 1p or 2p: ').upper() == '1P':
        # means server
        with server() as s:
            t = Thread(target=s.start)
            t.start()


            print('press any key to continue')
            msvcrt.getch()


            with client(*s.getIPandPort()) as c:
                c.setUserName(name)
                c.start()
    else:
        host, port = input('enter ip and port. (format ip:port):  ').split(':')
        print('{}:{}'.format(host, port))
        with client(host, int(port)) as c:
            c.setUserName(name)
            c.start()


