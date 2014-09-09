import ctypes
from ctypes import wintypes
from ctypes.wintypes import *

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
# COORD = wintypes._COORD


class COORD(wintypes._COORD):

    def __str__(self):
        return 'x={}, y={}'.format(super().X, super().Y)


class CONSOLE_FONT_INFO(ctypes.Structure):
    _fields_ = [('nFont', DWORD),
                ('dwFontSize', COORD)]


class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [('dwSize', COORD),
                ('dwCursorPosition', COORD),
                ('wAttributes', WORD),
                ('srWindow', SMALL_RECT),
                ('dwMaximumWindowSize', COORD)]


class dllLoader:

    '''
        load the dll written by c and call them for use
    '''

    def __init__(self):
        self._lib = {}

    def load(self, dll):
        dname = dll.__name__
        self._lib[dname] = ctypes.WinDLL(dll())
        return self._lib[dname]


dll = dllLoader()


@dll.load
def Kernel32():
    return 'Kernel32.dll'


@dll.load
def User32():
    return 'User32.dll'


@dll.load
def Gdi32():
    return 'Gdi32.dll'


def resizeConsoleWindow(hstdout,  width, height):
    '''
    by default, the console buffer is set to 80x300. This is only enough to cover the half of
    screen so the key point is to calculate the buffer size we need.

    screen resolution
    console font size

    buffer width size = screen resolution x / console font size x
    vice versa, the buffer height size

    '''
    hwnd = Kernel32.GetConsoleWindow()

    cfont_info = CONSOLE_FONT_INFO()
    cscreen_info = CONSOLE_SCREEN_BUFFER_INFO()

    Kernel32.GetCurrentConsoleFont(hstdout, False, ctypes.byref(cfont_info))
    Kernel32.GetConsoleScreenBufferInfo(hstdout, ctypes.byref(cscreen_info))

    print('font size:{} {}'.format(cfont_info.dwFontSize.X, cfont_info.dwFontSize.Y))
    print('screen buffer size:{} {}'.format(cscreen_info.dwSize.X, cscreen_info.dwSize.Y))
    size = COORD(width // cfont_info.dwFontSize.X, height // cfont_info.dwFontSize.Y)
    print(size)
    # by default, the font size in console is 8*16
    # bx = User32.GetSystemMetrics(5)  # CXBORDER
    # by = User32.GetSystemMetrics(6)  # CYBORDER
    # fx = User32.GetSystemMetrics(7)  # CXFIXEDFRAME
    # fy = User32.GetSystemMetrics(8)  # CYFIXEDFRAME
    # cpation_height = User32.GetSystemMetrics(51)  # CYSMCAPTION

    # rc = SMALL_RECT(0, 0, width // 8 -5, height // 16 - 5)
    Kernel32.SetConsoleScreenBufferSize(hstdout, size)
    # Kernel32.SetConsoleWindowInfo(hstdout, 1, ctypes.byref(rc))
    User32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE 3


class consoleBackBuffer:

    def __init__(self, w, h):
        self.mstdout = Kernel32.CreateConsoleScreenBuffer(
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


        Kernel32.SetConsoleScreenBufferSize(self.mstdout, self.coordBufSize)

        self.coordBufCoord = COORD(0, 0)

        self.readRgn = SMALL_RECT(0, 0, w - 1, h - 1)
        self.writeRgn = SMALL_RECT(0, 0, w - 1, h - 1)

        self.actuallyWritten = DWORD()  # used when writeconsole called

        self.setCursorVisibility()  # by default, set cursor invisible

    def setCursorVisibility(self, flag=False):
        self.cursorInfo.bVisible = flag
        Kernel32.SetConsoleCursorInfo(
            self.mstdout, ctypes.byref(self.cursorInfo))

    def toggleActiveConsole(self, stdout=None):
        if stdout is not None:
            Kernel32.SetConsoleActiveScreenBuffer(stdout)
        else:
            Kernel32.SetConsoleActiveScreenBuffer(self.mstdout)

    def getHandle(self):
        return self.mstdout

    def set_color(self, color):
        Kernel32.SetConsoleTextAttribute(self.mstdout, color)

    def gotoxy(self, x, y, stdout=None):
        coord = COORD(x, y)
        if stdout is None:
            Kernel32.SetConsoleCursorPosition(self.mstdout, coord)
        else:
            Kernel32.SetConsoleCursorPosition(stdout, coord)

    def setWriteSrc(self, x, y):
        self.writeRgn.Top = y
        self.writeRgn.Left = x
        self.writeRgn.Right = x + self.coordBufSize.X - 1
        self.writeRgn.Bottom = y + self.coordBufSize.Y - 1

    def textwrap(self, str, width):
        '''
            return a wrapped string
            this will split the string if it exceed the length of width
            ex. textwrap('hhhhhhh', 5)
            return r'hhhhh\nhh\n'
        '''
        strLst = []
        while len(str) > width:
            strLst.append(str[:width - 1])
            str = str[width - 1:]

        strLst.append(str)
        return '\n'.join(strLst) + '\n'

    def write(self, msg):
        msg = self.textwrap(msg, self.coordBufSize.X)
        success = Kernel32.WriteConsoleW(
            self.mstdout,
            msg,
            DWORD(len(msg)),
            ctypes.byref(self.actuallyWritten),
            None)

        if success == 0:
            myDebugMsg('WriteConsoleW failed')

    def present(self, mainBuffer):
        chiBuffer = (CHAR_INFO * (self.coordBufSize.X * self.coordBufSize.Y))()
        # the chiBuffer has different limited size according to heap size

        success = Kernel32.ReadConsoleOutputW(
            self.mstdout,
            ctypes.byref(chiBuffer),
            self.coordBufSize,
            self.coordBufCoord,
            ctypes.byref(self.readRgn)
        )

        if success == 0:
            myDebugMsg('ReadConsoleOutputW failed')

        success = Kernel32.WriteConsoleOutputW(
            mainBuffer,
            ctypes.byref(chiBuffer),
            self.coordBufSize,
            self.coordBufCoord,
            ctypes.byref(self.writeRgn))

        if success == 0:
            myDebugMsg('WriteConsoleOutput failed')

if __name__ == '__main__':
    hstdout = Kernel32.GetStdHandle(DWORD(-11))
    if(hstdout == HANDLE(-1)):
        print('get buffer handle failed')

    width = User32.GetSystemMetrics(0)
    height = User32.GetSystemMetrics(1)
    print(width, height)

    resizeConsoleWindow(hstdout, width, height)
