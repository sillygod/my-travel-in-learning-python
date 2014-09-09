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

    '''
    specify a flow control, every program should inherite this class to
    run.
    '''

    action = Action()

    def __init__(self, width, height):
        '''
        initial a pygame display
        '''
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE, 32)
        self.render = render(self.screen)
        self.control = Controller(App.action.eventType)

    def update(self):
        raise NotImplementedError

    def present(self):
        raise NotImplementedError

    def run(self):
        timer = pygame.time.Clock()
        while True:
            timer.tick(30)
            self.control.start(pygame.event.get())
            self.update()
            self.screen.fill((0, 0, 0))
            self.present()
            pygame.display.update()


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

            add border outside the rect region
            in order to fill the space of the corner,
            top and bottom border add extra length to fill that.

        '''
        canvas = pygame.Surface((widget.rect.width, widget.rect.height), pygame.SRCALPHA)
        canvas.fill(widget.bgColor, pygame.Rect(0, 0, widget.rect.width, widget.rect.height))

        if(isinstance(widget.borderRect['top'], pygame.Rect)):
            pygame.draw.rect(
                self._hdc, widget.border['color'], widget.borderRect['top'])
        if(isinstance(widget.borderRect['left'], pygame.Rect)):
            pygame.draw.rect(
                self._hdc, widget.border['color'], widget.borderRect['left'])
        if(isinstance(widget.borderRect['right'], pygame.Rect)):
            pygame.draw.rect(
                self._hdc, widget.border['color'], widget.borderRect['right'])
        if(isinstance(widget.borderRect['bottom'], pygame.Rect)):
            pygame.draw.rect(
                self._hdc, widget.border['color'], widget.borderRect['bottom'])

        self._hdc.blit(canvas, (widget.rect.x, widget.rect.y))

        for c in widget.content.values():
            self._hdc.blit(*c)  # unpack


class widget:

    '''
        this is a basic element of gui.
        I think it should contain some attributes..

        postition
        bg color
        border

        add detect if mouse pos is in the border or not...
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
            'border', {'top': 0, 'left': 0, 'right': 0, 'bottom': 0, 'color': (0, 0, 0)})
        self.borderRect = {'top': 0, 'left': 0, 'right': 0, 'bottom': 0}

        self.padding = kwargs.get(
            'padding', {'top': 0, 'left': 0, 'right': 0, 'bottom': 0})
        self.margin = kwargs.get(
            'padding', {'top': 0, 'left': 0, 'right': 0, 'bottom': 0})
        self.content = {}  # ex. [img, x, y]

        self.setBorder()

    def resize(self, width, height):
        self.rect.width, self.rect.height = width, height
        self.setBorder()  # reset border

    def move(self, x, y):
        '''update the all Rect's position'''
        self.rect.move_ip(x, y)
        for key in self.border:
            if key != 'color' and isinstance(self.border[key], pygame.Rect):
                self.border[key].move_ip(x, y)

    def setBorder(self):
        bdWidth = self.border['top']
        if bdWidth > 0:
            self.borderRect['top'] = pygame.Rect(
                self.rect.x - bdWidth, self.rect.y - bdWidth, self.rect.width + 2 * bdWidth, bdWidth)
        bdWidth = self.border['left']
        if bdWidth > 0:
            self.borderRect['left'] = pygame.Rect(
                self.rect.x - bdWidth, self.rect.y, bdWidth, self.rect.height)
        bdWidth = self.border['right']
        if bdWidth > 0:
            self.borderRect['right'] = pygame.Rect(
                self.rect.right, self.rect.y, bdWidth, self.rect.height)
        bdWidth = self.border['bottom']
        if bdWidth > 0:
            self.borderRect['bottom'] = pygame.Rect(
                self.rect.x - bdWidth, self.rect.bottom, self.rect.width + 2 * bdWidth, bdWidth)

    def isPosIn(self, pos):
        return self.rect.collidepoint(pos)

    def update(self):
        raise NotImplementedError()


class wImage(widget):

    '''
    '''

    def __init__(self, fname=None, **kwargs):
        super().__init__(**kwargs)
        if fname is not None:
            self.img = pygame.image.load(fname)
            self.resize_img = None
            self.alpha = 255
            self.resize(self.rect.width, self.rect.height)

    def resize(self, width, height):
        super().resize(width, height)
        self.resize_img = pygame.transform.scale(
            self.img, (self.rect.width, self.rect.height))

        self.content['image'] = [self.resize_img, (self.rect.x, self.rect.y)]

    def setAlpha(self, value):
        self.resize_img.set_alpha(value)
        self.content['image'] = [self.resize_img, (self.rect.x, self.rect.y)]

    def copyFromImg(self, image):
        self.img = image
        self.resize(self.rect.width, self.rect.height)

    def getSurface(self):
        return self.resize_img


class Window:

    '''
    '''

    def __init__(self):
        pass


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
            'in': kwargs.get('mouse_in', (255, 150, 55)),
            'out': kwargs.get('mouse_out', (255, 150, 55, 100)),
            'press': kwargs.get('mouse_press', (100, 50, 100))}

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
        show a brief string

    note:
        maybe it needs a object responsible for
        font's position and size
    '''

    def __init__(self, text=None, **kwargs):
        super().__init__(**kwargs)
        self.font_size = kwargs.get('font_size', 20)
        if text is not None:
            self.text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        font = SysFont('consola', self.font_size)
        self._font = font.render(self._text, True, (255, 0, 0))
        self.content['font'] = [self._font, (
            self.rect.centerx - self._font.get_width() / 2,
            self.rect.centery - self._font.get_height() / 2)]


class ListBox(widget):

    '''
    contain a list of label?

    ------------  after click ------------
    |content|\/|      =>      |content|\/|
    ------------              |content   |
                              |content   |
                              |content   |
                              ......
                              ---------

    '''

    def __init__(self, valueList, **kwargs):
        self._list = [Label(text) for text in valueList if isinstance(text, str)]

    def expand(self):
        pass

    def collapse(self):
        pass


class inputLabel(widget):

    '''
    '''

    def __init__(self, **kwargs):
        pass


def main():
    class MyApp(App):

        '''
        '''
        def __init__(self, width, height):
            super().__init__(width, height)
            self.btn = Button(x=20, y=400, width=100, height=100,
                              border={'top': 5, 'left': 5, 'right': 5, 'bottom': 5, 'color': (128, 30, 30)},
                              mouse_in=(50, 100, 123),
                              mouse_out=(50, 100, 123, 100),
                              mouse_press=(50, 100, 103))
            self.btn.text = 'save'

            self.title = Label('This is a imageCropper', x=200, y=10, width=300, height=30,
                               border={'top': 5, 'left': 0, 'right': 0, 'bottom': 0, 'color': (70, 100, 50)},
                               bgColor=(125, 20, 80))

            self.crop = cropRect(x=200, y=50, width=300, height=300)
            self.crop.loadImg('World.png')

            self.previewPic = wImage(x=600, y=50, width=150, height=150)

            self.btn.setAction(
                lambda: pygame.image.save(self.previewPic.getSurface(), 'test.png'))

        def update(self):
            self.crop.update()
            self.previewPic.copyFromImg(self.crop.retCropImg())
            self.btn.update()

        def present(self):
            self.render.render(self.crop)
            self.render.render(self.previewPic)
            self.render.render(self.btn)
            self.render.render(self.title)


    class cropRect(widget):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.img = None
            self.displayImg = None
            self.cursor = Cursor()
            self.crop = wImage(x=50, y=50, width=150, height=150,
                               border={'top': 3, 'left': 3, 'right': 3, 'bottom': 3, 'color': (30, 30, 30)})
            self.hdc = pygame.Surface(
                (self.rect.width, self.rect.height), pygame.SRCALPHA)

            self._render = render(self.hdc)  # inner render for std widget

            self.moveable = False
            self.resizeable = False

            @App.action.connect
            def onMouseMove():
                pos = pygame.mouse.get_pos()
                delpos = pygame.mouse.get_rel()
                # offset coordinate
                pos = (pos[0] - self.rect.x, pos[1] - self.rect.y)
                if self.isInBorder(pos):
                    self.cursor.setCursor('resize_H')
                elif self.crop.isPosIn(pos):
                    self.cursor.setCursor('move')
                else:
                    self.cursor.setCursor('arrow')

                if self.moveable:
                    self.crop.move(*delpos)
                    self.updateCrop()
                if self.resizeable:
                    self.crop.resize(self.crop.rect.width + delpos[0],
                                     self.crop.rect.height + delpos[1])
                    self.updateCrop()

            @App.action.connect
            def onMouseButtonDown():
                pos = pygame.mouse.get_pos()
                pos = (pos[0] - self.rect.x, pos[1] - self.rect.y)
                # offset coordinate
                if self.isInBorder(pos):
                    self.resizeable = True
                elif self.crop.isPosIn(pos):
                    self.moveable = True

            @App.action.connect
            def onMouseButtonUP():
                self.moveable = False
                self.resizeable = False

        def isInBorder(self, pos):
            for key in self.crop.borderRect:
                if key != 'color' and self.crop.borderRect[key].collidepoint(pos):
                    return True
            return False

        def loadImg(self, fname):
            self.img = wImage(
                fname, x=0, y=0, width=self.rect.width, height=self.rect.height)
            self.displayImg = wImage(
                x=0, y=0, width=self.rect.width, height=self.rect.height)
            self.updateCrop()

        def updateCrop(self):
            forceInside(
                pygame.Rect(0, 0, self.rect.width, self.rect.height), self.crop.rect)
            self.crop.copyFromImg(self.img.resize_img.subsurface(self.crop.rect))
            self.displayImg.copyFromImg(self.img.resize_img)
            self.displayImg.setAlpha(120)

        def retCropImg(self):
            '''return a crop Image '''
            return self.crop.resize_img

        def update(self):
            self.hdc.fill((0, 0, 0))  # well, note this haha
            self._render.render(self.displayImg)
            self._render.render(self.crop)
            self.content['surface'] = [self.hdc, (self.rect.x, self.rect.y)]

    obj = MyApp(860, 640)
    obj.run()


if __name__ == "__main__":
    main()
