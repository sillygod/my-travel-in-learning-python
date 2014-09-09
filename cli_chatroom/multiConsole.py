'''
    use the windows api to implement my CLI

    msdn
    http://msdn.microsoft.com/en-us/library/windows/desktop/ms684965%28v=vs.85%29.aspx

    try to use double console mode
    http://msdn.microsoft.com/en-us/library/windows/desktop/ms685032%28v=vs.85%29.aspx

    a ctype tutorial
    http://python.net/crew/theller/ctypes/tutorial.html


    sys.stdout = file object


    dll.Kernel32.SetConsoleActiveScreenBuffer(hNewScreenBuffer)


'''


from ctypes.wintypes import *
import msvcrt
from console import consoleBackBuffer
from console import Kernel32
from console import User32
from console import resizeConsoleWindow
import inspect


def myDebugMsg(msg=''):
    print('{}   at:{}'.format(msg, inspect.stack()[1][1:3]))
    input()


def pause():
    while True:
        if msvcrt.kbhit():
            break


class widget:

    def __init__(self, sx, sy, w, h):
        self.console = consoleBackBuffer(w, h)
        self.console.setWriteSrc(sx, sy)
        self.gx = sx
        self.gy = sy
        #global position
        self.w = w
        self.h = h
        self.mTitle = 'no name'
        self.content = []

    def getConsole(self):
        return self.console

    def getContent(self):
        return self.content[:]

    def setContent(self, content):
        self.content = content[:]

    def setTitle(self, title):
        self.mTitle = title

    def getTitle(self):
        return self.mTitle

    title = property(getTitle, setTitle)

    def addContent(self, s):
        if len(s) >= self.w - 3:
            self.content.append(s[:self.w - 3])
            self.content.append(s[self.w - 3:])
        else:
            self.content.append(s)

    def delContent(self, s):
        self.content.remove(s)

    def display(self, stdout):
        self.console.present(stdout)


class usermenu(widget):

    '''
        show user list
    '''

    def __init__(self, sx, sy, w, h):
        super().__init__(sx, sy, w, h)

    def update(self):
        # draw outline
        border = '|' + '-' * (self.w - 2) + '|'
        emptyLine = '|' + ' ' * (self.w - 2) + '|'
        for y in range(self.h):
            if y in (0, 2, self.h - 1):
                self.console.write(border)
            else:
                self.console.write(emptyLine)

        # draw title and user list
        tx = int((self.w - len(self.title)) / 2)
        self.console.gotoxy(tx, 1)
        self.console.write(self.title)

        for i in range(len(self.content)):
            self.console.gotoxy(2, 3 + i)
            self.console.write(self.content[i])
        self.console.gotoxy(0, 0)


class msgroom(widget):

    def __init__(self, sx, sy, w, h):
        super().__init__(sx, sy, w, h)
        self.scroll = 0
        self.start = 0

    def scrollContent(self, offset):
        self.scroll += offset
        if self.scroll > 0:
            self.scroll = 0

    def detectPageUpAndDown(self):
        pageUP = User32.GetAsyncKeyState(0x21)
        pageDown = User32.GetAsyncKeyState(0x22)

        if pageUP != 0:
            self.scrollContent(-2)
        if pageDown != 0:
            self.scrollContent(2)

    def update(self):
        self.detectPageUpAndDown()
        border = '|' + '-' * (self.w - 2) + '|'
        emptyLine = '|' + ' ' * (self.w - 2) + '|'

        for y in range(self.h):
            if y in (0, 2, self.h - 1):
                self.console.write(border)
            else:
                self.console.write(emptyLine)
        # draw title and content
        tx = int((self.w - len(self.title)) / 2)
        self.console.gotoxy(tx, 1)
        self.console.write(self.title)

        index = len(self.content) - (self.h - 4) + self.scroll
        self.start = 0 if index < 0 else index

        obj = self.content if len(
            self.content) < self.h - 4 else self.content[self.start: self.start + self.h - 4]
        # wow, slice in python seems to automatically check the index if it is out of range
        # ex. lst = [1,2,3,4,5]
        # lst[-6:] no error produce

        for i in range(len(obj)):
            self.console.gotoxy(1, 3 + i)
            self.console.write(obj[i])
        self.console.gotoxy(0, 0)


class inputLabel(widget):

    def __init__(self, sx, sy, w, h):
        super().__init__(sx, sy, w, h)

    def update(self):
        border = '|' + '-' * (self.w - 2) + '|'
        emptyLine = '|' + ' ' * (self.w - 2) + '|'

        for y in range(self.h):
            if y in (0, 2, self.h - 1):
                self.console.write(border)
            else:
                self.console.write(emptyLine)

        tx = int((self.w - 8))
        self.console.gotoxy(tx, 0)
        self.console.write('|')
        self.console.gotoxy(tx, 2)
        self.console.write('|')
        self.console.gotoxy(tx, 1)
        self.console.write('|submit')
        self.console.gotoxy(0, 0)


def test():
    '''
    there is a way to resize the console buffer...
    now, it's still in test stage to understand the winapi's work
    '''
    hstdout = Kernel32.GetStdHandle(DWORD(-11))
    if(hstdout == HANDLE(-1)):
        print('create buffer failed')

    width = 1024
    height = 690
    # resizeConsoleWindow(hstdout, width, height)

    backBuffer = consoleBackBuffer(180, 80)

    userpanel = usermenu(56, 0, 15, 17)
    userpanel.title = 'user list'
    userpanel.addContent('heyhey')
    userpanel.addContent('haha')
    userpanel.update()
    userpanel.display(backBuffer.getHandle())

    chatroom = msgroom(0, 0, 55, 17)
    chatroom.title = 'chat room'
    chatroom.addContent("eric: I'm so happy")
    chatroom.update()
    chatroom.display(backBuffer.getHandle())

    inLabel = inputLabel(0, 18, 71, 3)
    inLabel.update()
    inLabel.display(backBuffer.getHandle())

    backBuffer.present(hstdout)
    input()


if __name__ == '__main__':
    test()
