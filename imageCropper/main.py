import pygame
import sys
from pygame.locals import *
import os
from pygame.font import SysFont
# TODO
# first, add some simple gui wiget like button, label, ect.
# second, to think how to make gui wdiget beautiful structure


class Action():

    '''
        FUNC:
            as a adapter, to connect an object and an action
            should it be an member of app class? or just a global object

        note:
            write connect in the object __init__ method to get the self(this) attribute
            that's now solution...
    '''
    eventType = {'onKeyDown': [],
                 'onMouseButtonDown': [],
                 'onMouseMove': [],
                 'onMouseButtonUP': []}

    def __init__(self):
        pass

    def connect(self, *args):
        '''
            usage:
            @xx.connect
            def anything():
                pass
        '''
        _func = args[0]
        Action.eventType[_func.__name__].append(_func)


class Controller:

    '''
        handle for the event queue
    '''

    def __init__(self, event):
        self.event = event  # action.eventType

    def start(self, eventList):
        for e in eventList:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                for func in self.event['onKeyDown']:
                    func(e.key)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                for func in self.event['onMouseButtonDown']:
                    func()
            elif e.type == pygame.MOUSEBUTTONUP:
                for func in self.event['onMouseButtonUP']:
                    func()
            elif e.type == pygame.MOUSEMOTION:
                for func in self.event['onMouseMove']:
                    func()


class App:

    action = Action()

    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

        self.realBG = pygame.Surface((width, height), pygame.SRCALPHA)
        self.realBG.fill((0, 0, 0, 100), (0, 0, width, height))

        self.render = render(self.realBG)
        self.btn = Button(x=300, y=100, width=100, height=100)
        self.btn.text = 'save'

        self.img = wImage('World.png', x=20, y=20, width=200, height=200)

        self.control = Controller(App.action.eventType)

        self.btn.setAction(
            lambda: pygame.image.save(self.previewPic, 'test.png'))
        # @App.action.connect
        # def onKeyDown(key):
        #     if key == K_s:
        #         pygame.image.save(self.previewPic, 'test.png')

    def update(self):
        self.btn.update()

    def present(self):

        self.render.render(self.img)
        self.render.render(self.btn)
        self.screen.blit(self.realBG, (0, 0))
        pygame.display.update()

    def run(self):

        timer = pygame.time.Clock()
        while True:
            timer.tick(30)
            self.control.start(pygame.event.get())
            self.update()
            self.present()


class Cursor:

    def __init__(self):

        self.moveString = (  # 24X16--width x height--this is the standard in pygame
            "           XX           ",
            "          X..X          ",
            "         X....X         ",
            "           ..           ",
            "     X     ..     X     ",
            "    X.     ..     .X    ",
            "   X................X   ",
            "   X................X   ",
            "    X.     ..     .X    ",
            "     X     ..     X     ",
            "           ..           ",
            "         X....X         ",
            "          X..X          ",
            "           XX           ",
            "                        ",
            "                        ",
        )

        self.stringType = {
            'arrow': pygame.cursors.arrow,
            'move': self.moveString,
            'resize_H': pygame.cursors.sizer_x_strings,
            'resize_V': pygame.cursors.sizer_y_strings,
            'resize_upLtTobotRt': pygame.cursors.sizer_xy_strings,
            'resize_upRtTobotLt': pygame.cursors.sizer_xy_strings[13::-1] + pygame.cursors.sizer_xy_strings[14:]
        }

    def setCursor(self, type):
        if isinstance(self.stringType[type][0], str):
            string = self.stringType[type]
            cursor = pygame.cursors.compile(string)
            size = (len(string[0]), len(string))
            hotspot = (int(size[0] / 2), int(size[1] / 2))
            pygame.mouse.set_cursor(size, hotspot, *cursor)
        else:
            pygame.mouse.set_cursor(*self.stringType[type])


class posRecorder:

    def __init__(self, x=0, y=0):
        self.pos = (x, y)
        self.delX = 0
        self.delY = 0

    def getDelta(self):
        delX, delY = self.delX, self.delY
        self.delX, self.delY = 0, 0
        return (delX, delY)

    def curPos(self, pos):
        self.delX = pos[0] - self.pos[0]
        self.delY = pos[1] - self.pos[1]
        self.pos = (pos[0], pos[1])

    def lastPos(self, pos):
        self.pos = pos


def forceInside(forceScope, rect):
    if rect.left < forceScope.left:
        rect.left = forceScope.left
    if rect.top < forceScope.top:
        rect.top = forceScope.top
    if rect.left + rect.width > forceScope.left + forceScope.width:
        rect.left = (forceScope.left + forceScope.width) - rect.width
    if rect.top + rect.height > forceScope.top + forceScope.height:
        rect.top = (forceScope.top + forceScope.height) - rect.height


class widget:

    '''
        this is a basic element of gui.
        I think it should contain some attributes..

        postition
        bg color
        border

        and even need some behavior like detect mouse and keyboard aciton..
    '''

    def __init__(self, **kwargs):
        '''
            x
            y
            width
            height
            border
            background color
        '''
        self.rect = pygame.Rect(kwargs.get('x', 0),
                                kwargs.get('y', 0),
                                kwargs.get('width', 0),
                                kwargs.get('height', 0))
        self.bgColor = kwargs.get('bgColor', (0, 0, 0))
        self.border = kwargs.get(
            'border', {'top': 5, 'left': 5, 'right': 5, 'bottom': 5, 'color': (120, 20, 30)})
        self.padding = kwargs.get(
            'padding', {'top': 0, 'left': 0, 'right': 0, 'bottom': 0})
        self.margin = kwargs.get(
            'padding', {'top': 0, 'left': 0, 'right': 0, 'bottom': 0})
        self.content = {}  # ex. [img, x, y]

    def isPosIn(self, pos):
        return self.rect.collidepoint(pos)

    def update(self):
        raise NotImplementedError


class wImage(widget):

    '''
    '''

    def __init__(self, fname, **kwargs):
        super().__init__(**kwargs)
        self.img = pygame.transform.scale(pygame.image.load(fname),
                                         (self.rect.width, self.rect.height))
        self.content['image'] = [self.img, (self.rect.x, self.rect.y)]


class render:

    '''
        responsible for the display of gui widget
        I think there should be an object as a Controller
        it can receive the data from the widget and then
        draw its outline on the window
    '''

    def __init__(self, screen):
        self._hdc = screen  # get the DC

    def render(self, widget):
        ''' draw background first
            then border
            content ex. image, font, etc.
        '''
        self._hdc.fill(widget.bgColor, widget.rect)
        if(widget.border['top'] > 0):
            pygame.draw.line(self._hdc, widget.border['color'],
                            (widget.rect.x, widget.rect.y),
                            (widget.rect.right, widget.rect.y),
                             widget.border['top'])
        if(widget.border['left'] > 0):
            pygame.draw.line(self._hdc, widget.border['color'],
                            (widget.rect.x, widget.rect.y),
                            (widget.rect.x, widget.rect.bottom),
                             widget.border['left'])
        if(widget.border['right'] > 0):
            pygame.draw.line(self._hdc, widget.border['color'],
                            (widget.rect.right, widget.rect.y),
                            (widget.rect.right, widget.rect.bottom),
                             widget.border['right'])
        if(widget.border['bottom'] > 0):
            pygame.draw.line(self._hdc, widget.border['color'],
                            (widget.rect.x, widget.rect.bottom),
                            (widget.rect.right, widget.rect.bottom),
                             widget.border['bottom'])
        for c in widget.content.values():
            self._hdc.blit(*c)  # unpack


class Window:

    '''
    '''

    def __init__(self):
        pass


class cropRect(widget):

    def __init__(self, width, height, sx, sy):
        super().__init__(width, height, sx, sy)
        self.moveRect = pygame.Rect(
            self.rect.left + 20,
            self.rect.top + 20,
            self.rect.width - 40,
            self.rect.height - 40)

        self.cursor = Cursor()
        self.recorder = posRecorder()
        self.moveable = False
        self.resizeable = False

        @App.action.connect
        def onMouseButtonUP():
            self.moveable = False
            self.resizeable = False

        @App.action.connect
        def onMouseButtonDown():
            pos = pygame.mouse.get_pos()
            if self.isMouseIn(pos):
                if self.moveRect.collidepoint(pos):
                    self.moveable = True
                else:
                    self.resizeable = True
                self.recorder.lastPos(pos)

        @App.action.connect
        def onMouseMove():
            pos = pygame.mouse.get_pos()
            if self.isMouseIn(pos):
                if self.moveRect.collidepoint(pos):
                    self.cursor.setCursor('move')
                else:
                    self.cursor.setCursor('resize_H')
            else:
                self.cursor.setCursor('arrow')

            if self.moveable or self.resizeable:
                self.recorder.curPos(pos)

    def adjustMoveRect(self):
        self.moveRect = pygame.Rect(
            self.rect.left + 5,
            self.rect.top + 5,
            self.rect.width - 10,
            self.rect.height - 10)

    def update(self):  # here need to redraw
        delX, delY = self.recorder.getDelta()
        if self.moveable:
            self.rect.move_ip(delX, delY)
        elif self.resizeable:
            self.rect.width += delX
            self.rect.height += delY

    def present(self, mainSurface):
        self.fill((0, 0, 0, 100), self._rect)
        super().present(mainSurface)


class Button(widget):

    '''
        a button widget can be clicked to cause an action
        and a button can be displayed by image or text(is centered by default)

        now, need to consider some point...
        1. decide the button size which is depended on content(ex. text, img, etc..)
        2. border size
        3. padding size
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._state = ''
        self._style = {
            'in': (105, 20, 20, 10), 'out': (50, 50, 55, 10), 'press': (255, 0, 0)}

        self._text = ''
        self._action = None  # a function object

        @App.action.connect
        def onMouseMove():
            pos = pygame.mouse.get_pos()
            if self.isPosIn(pos):
                self._state = 'in'
            else:
                self._state = 'out'

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        font = SysFont('consola', 60)
        self._font = font.render(self._text, True, (255, 0, 0))
        # well, figure out what the font's width is depended on
        self.content['font'] = [self._font,
                                (self.rect.centerx - self._font.get_width() / 2, self.rect.centery - self._font.get_height() / 2)]

    def setAction(self, action):
        @App.action.connect
        def onMouseButtonDown():
            pos = pygame.mouse.get_pos()
            if self.isPosIn(pos):
                self._state = 'press'
                action()

    def update(self):
        self.bgColor = self._style[self._state]


class Label(widget):

    '''
        FUNC:

    '''

    def __init__(self, **kwargs):
        pass


if __name__ == "__main__":
    obj = App(860, 640)
    obj.run()
