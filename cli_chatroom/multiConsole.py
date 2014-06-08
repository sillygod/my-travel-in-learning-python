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


import ctypes
from ctypes import wintypes
from ctypes.wintypes import *
import msvcrt
import sys


#-----------------debug use----------------------
import inspect


def myDebugMsg(msg=''):
    print('{}   at:{}'.format(msg, inspect.stack()[1][1:3]))


def pause():
    while True:
        if msvcrt.kbhit():
            break
#------------------------------------------------


#--------------------------------------------------
# use ctypes to create a windows data type
class Char(ctypes.Union):
    _fields_ = [("UnicodeChar", WCHAR),
                ("AsciiChar", CHAR)]


class CHAR_INFO(ctypes.Structure):
    _anonymous_ = ("Char",)
    _fields_ = [("Char", Char),
                ("Attributes", WORD)]


class CONSOLE_CURSOR_INFO(ctypes.Structure):
    _fields_ = [('dwSize', DWORD),
                ('bVisible', BOOL)]


PCHAR_INFO = ctypes.POINTER(CHAR_INFO)
COORD = wintypes._COORD
#---------------------------------------------------


class dllLoader:

    '''
        load the dll written by c and call them for use
    '''

    def __init__(self):
        self.mKernel32 = ctypes.WinDLL('Kernel32.dll')
        self.mUser32 = ctypes.WinDLL('User32.dll')
        self.mGdi32 = ctypes.WinDLL('Gdi32.dll')

    def getKernel32(self):
        return self.mKernel32

    def getUser32(self):
        return self.mUser32

    def getGdi32(self):
        return self.mGdi32

    Kernel32 = property(getKernel32)
    User32 = property(getUser32)
    Gdi32 = property(getGdi32)


dll = dllLoader()

#-------------------------------------------------------


class consoleBackBuffer:

    def __init__(self, w, h):
        self.mstdout = dll.Kernel32.CreateConsoleScreenBuffer(
            0x80000000 | 0x40000000,  # generic read and write
            0x00000001 | 0x00000002,
            None,
            1,  # CONSOLE_TEXTMODE_BUFFER defined in winbase.h
            None)
        if self.mstdout == HANDLE(-1):
            myDebugMsg('CreateConsoleScreenBuffer failed')

        self.cursorInfo = CONSOLE_CURSOR_INFO()
        self.cursorInfo.dwSize = 25

        self.coordBufSize = COORD(w, h)

        dll.Kernel32.SetConsoleScreenBufferSize(self.mstdout, self.coordBufSize)

        self.coordBufCoord = COORD(0, 0)

        self.readRgn = SMALL_RECT(0, 0, w-1, h-1)
        self.writeRgn = SMALL_RECT(0, 0, w-1, h-1)

        self.actuallyWritten = DWORD()  # used when writeconsole called

        self.setCursorVisibility()  # by default, set cursor invisible

    def setCursorVisibility(self, flag=False):
        self.cursorInfo.bVisible = flag
        dll.Kernel32.SetConsoleCursorInfo(
            self.mstdout, ctypes.byref(self.cursorInfo))

    def toggleActiveConsole(self, stdout=None):
        if stdout is not None:
            dll.Kernel32.SetConsoleActiveScreenBuffer(stdout)
        else:
            dll.Kernel32.SetConsoleActiveScreenBuffer(self.mstdout)

    def getHandle(self):
        return self.mstdout

    def set_color(self, color):
        dll.Kernel32.SetConsoleTextAttribute(self.mstdout, color)

    def gotoxy(self, x, y, stdout=None):
        coord = COORD(x, y)
        if stdout is None:
            dll.Kernel32.SetConsoleCursorPosition(self.mstdout, coord)
        else:
            dll.Kernel32.SetConsoleCursorPosition(stdout, coord)

    def setWriteSrc(self, x, y):
        self.writeRgn.Top = y
        self.writeRgn.Left = x
        self.writeRgn.Right = x + self.coordBufSize.X - 1
        self.writeRgn.Bottom = y + self.coordBufSize.Y - 1

    def write(self, msg):
        while len(msg) > self.coordBufSize.X:

            tempMsg = msg[:self.coordBufSize.X - 1] + '\n'
            msg = msg[self.coordBufSize.X - 1:]

            success = dll.Kernel32.WriteConsoleW(
                self.mstdout,
                tempMsg,
                DWORD(len(tempMsg)),
                ctypes.byref(self.actuallyWritten),
                None)

            if success == 0:
                myDebugMsg('WriteConsoleW failed')

        if '\n' not in msg:
            msg = msg + '\n'

        if len(msg) != 0:
            success = dll.Kernel32.WriteConsoleW(
                self.mstdout,
                msg,
                DWORD(len(msg)),
                ctypes.byref(self.actuallyWritten),
                None)

            if success == 0:
                myDebugMsg('WriteConsoleW failed')

    def present(self, mainBuffer):
        chiBuffer = (CHAR_INFO * (self.coordBufSize.X * self.coordBufSize.Y))()

        success = dll.Kernel32.ReadConsoleOutputW(
            self.mstdout,
            ctypes.byref(chiBuffer),
            self.coordBufSize,
            self.coordBufCoord,
            ctypes.byref(self.readRgn)
        )

        if success == 0:
            myDebugMsg('ReadConsoleOutputW failed')

        success = dll.Kernel32.WriteConsoleOutputW(
            mainBuffer,
            ctypes.byref(chiBuffer),
            self.coordBufSize,
            self.coordBufCoord,
            ctypes.byref(self.writeRgn))

        if success == 0:
            myDebugMsg('WriteConsoleOutput failed')


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
        pageUP = dll.User32.GetAsyncKeyState(0x21)
        pageDown = dll.User32.GetAsyncKeyState(0x22)

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
    from threading import Timer, Thread

    hstdout = dll.Kernel32.GetStdHandle(DWORD(-11))
    hwnd = dll.Kernel32.GetConsoleWindow()
    if(hstdout == HANDLE(-1)):
        print('create buffer failed')
    # size = COORD(490//8+1, 690//16+1)
    # rc = SMALL_RECT(0, 0, 490//8, 690//16)
    # dll.Kernel32.SetConsoleWindowInfo(hstdout, 1, ctypes.byref(rc))
    # dll.Kernel32.SetConsoleScreenBufferSize(hstdout, size)
    # hrgn = dll.Gdi32.CreateRectRgn(20, 20, size.X, size.Y)
    # dll.User32.SetWindowRgn(hwnd, hrgn, 1)


    backBuffer = consoleBackBuffer(80, 25)

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
