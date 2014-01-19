import pygame
import sys
from pygame.locals import *
import os


# TODO
# first, refactor this code
# second, add some simple gui wiget like button, label, ect.


class Action():

    '''
        FUNC:
            as a adapter, to connect an object and an action
            should it be an member of app class? or just a global object
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

        self.crop = cropRect(200, 200, 0, 0)
        img = pygame.image.load('World.png')
        self.bg = widget(640, 480, 0, 0)
        self.bg.setImg(img)

        self.previewPic = widget(150, 150, 700, 20)
        self.control = Controller(App.action.eventType)

        @App.action.connect
        def onKeyDown(key):
            if key == K_s:
                pygame.image.save(self.previewPic, 'test.png')

    def update(self):
        self.crop.update()
        forceInside(self.bg.get_rect(), self.crop.rect)
        self.crop.adjustMoveRect()

    def present(self):
        self.screen.blit(self.realBG, (0, 0))
        self.bg.present(self.screen)
        self.crop.present(self.screen)
        tmp = self.bg.subsurface(self.crop.rect)
        self.previewPic.setImg(tmp)
        self.previewPic.present(self.screen)

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
            'arrow': pygame.cursors.thickarrow_strings,
            'move': self.moveString,
            'resize_H': pygame.cursors.sizer_x_strings,
            'resize_V': pygame.cursors.sizer_y_strings,
            'resize_upLtTobotRt': pygame.cursors.sizer_xy_strings,
            'resize_upRtTobotLt': pygame.cursors.sizer_xy_strings[13::-1] + pygame.cursors.sizer_xy_strings[14:]
        }

    def setCursor(self, type):
        string = self.stringType[type]
        cursor = pygame.cursors.compile(string)
        size = (len(string[0]), len(string))
        hotspot = (int(size[0] / 2), int(size[1] / 2))
        pygame.mouse.set_cursor(size, hotspot, *cursor)


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
    elif rect.top < forceScope.top:
        rect.top = forceScope.top
    elif rect.left + rect.width > forceScope.left + forceScope.width:
        rect.left = (forceScope.left + forceScope.width) - rect.width
    elif rect.top + rect.height > forceScope.top + forceScope.height:
        rect.top = (forceScope.top + forceScope.height) - rect.height


class widget(pygame.Surface):

    '''
        pygame.Surface is similiar to the Device Content
        so maybe it's not a good idea to use this class as
        a widget for GUI?

        a base class handle for device context...
    '''

    def __init__(self, width, height, sx, sy):
        super().__init__((width, height), pygame.SRCALPHA)  # good!! I deal it

        self.rect = self.get_rect()  # get_rect() return a new rect!
        self.cursor = Cursor()
        self.rect.top = sy
        self.rect.left = sx

    def isMouseIn(self, pos):
        return self.rect.collidepoint(pos)

    def setImg(self, img):
        ''' here use (0,0) because it blit in itself'''
        self.blit(pygame.transform.scale(
            img, (self.rect.width, self.rect.height)), (0, 0))

    def present(self, mainSurface):
        mainSurface.blit(pygame.transform.scale(
            self, (self.rect.width, self.rect.height)), self.rect.topleft)


class cropRect(widget):

    def __init__(self, width, height, sx, sy):
        super().__init__(width, height, sx, sy)
        self.moveRect = pygame.Rect(
            self.rect.left + 20,
            self.rect.top + 20,
            self.rect.width - 40,
            self.rect.height - 40)

        self.fill((0, 0, 0, 100), (0, 0, self.rect.width, self.rect.height))
        self.fill((255, 255, 255, 100),
                  (20, 20, self.moveRect.width, self.moveRect.height))

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
            print(self.rect, self.moveRect)
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
            self.rect.left + 20,
            self.rect.top + 20,
            self.rect.width - 40,
            self.rect.height - 40)

    def update(self):
        delX, delY = self.recorder.getDelta()
        if self.moveable:
            self.rect.move_ip(delX, delY)
        elif self.resizeable:
            self.rect.width += delX
            self.rect.height += delY


class Button(widget):

    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    obj = App(860, 640)
    obj.run()
