

import pygame
import sys
from pygame.locals import *

#main process class
class App:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.obj1 = imgObject(200,200, 0, 20)
        self.realBG = pygame.Surface( (width, height), pygame.SRCALPHA)
        self.realBG.fill((0,0,0,100),(0,0,width, height))
        self.bg = imgObject(640, 480, 0, 0, 'World.png')
        self.previewPic = imgObject(150, 150, 700, 20)


        
        self.control = eventController()
        
        @self.control.event
        def onKeyDown(key):
            if key == K_s:
                pygame.image.save(self.previewPic, 'test.png')
        
        @self.control.event
        def onMouseMove():
            self.obj1.mouseMove()

        @self.control.event
        def onMouseDown():
            self.obj1.mouseButtonDown()

        @self.control.event
        def onMouseUP():
            self.obj1.mouseButtonUP()

    
    
    def present(self):
        self.screen.blit( self.realBG, (0,0) )
        self.bg.present(self.screen)
        self.obj1.present(self.screen)
        tmp = self.bg.subsurface(self.obj1.getRect())
        self.previewPic.setImg(tmp)
        self.previewPic.present(self.screen)
        
        pygame.display.update()
    
    
    def run(self):
        timer = pygame.time.Clock()
        while True:
            timer.tick(30)
            self.control.start(pygame.event.get())
            self.present()
            
  

#event control class      
class eventController:
    def __init__(self):
        
        self.eventFunc = {
        'onKeyDown' : self.useless,
        'onMouseDown' : self.useless,
        'onMouseMove' : self.useless,
        'onMouseUP' : self.useless
        }
        # the key name should be the one of the following
        # onKeyDown
        # onMouseDown
        # onMouseUP
        # onMouseMove
        
    def start(self, eventList):
        for e in eventList:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                self.eventFunc['onKeyDown'](e.key)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                self.eventFunc['onMouseDown']()
            elif e.type == pygame.MOUSEBUTTONUP:
                self.eventFunc['onMouseUP']()
            elif e.type == pygame.MOUSEMOTION:
                self.eventFunc['onMouseMove']()
    
    def useless(self, *args):
        ''' 
            be used in the initialization of eventFunc.. the None can't be used here
            because it's non-callable
        '''
        pass
    
    def event(self, *args):
        func = args[0]
        name = func.__name__
        self.eventFunc[name]=func
        

        
class Cursor:
    def __init__(self):
        
        
        self.moveString =( #24X16--width x height--this is the standard in pygame
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
            'arrow' : pygame.cursors.thickarrow_strings,
            'move' : self.moveString,
            'resize_H' : pygame.cursors.sizer_x_strings,
            'resize_V' : pygame.cursors.sizer_y_strings,
            'resize_upLtTobotRt' : pygame.cursors.sizer_xy_strings,
            'resize_upRtTobotLt' : pygame.cursors.sizer_xy_strings[13::-1]+pygame.cursors.sizer_xy_strings[14:]
        }
    
    
    def setCursor(self, type):
        string = self.stringType[type]
        cursor = pygame.cursors.compile(string)
        size = ( len(string[0]), len(string) )
        hotspot = (int(size[0]/2), int(size[1]/2))
        pygame.mouse.set_cursor(size,hotspot,*cursor)
        


class tuplePos:
    def __init__(self, x=0, y=0):
        self.pos = (x, y)

    def setStartPos(self, pos):
        self.pos = pos

    def getDelta(self, pos):
        delX = pos[0] - self.pos[0] 
        delY = pos[1] - self.pos[1]
        self.pos = (pos[0], pos[1])
        return (delX, delY)

class robustRect(pygame.Rect):
    def __init__(self, forceScope, left, top, width, height):
        super().__init__(left, top, width, height)
        self.forceScope = forceScope # this is the location that can't be exceed

    def forceInside(self):
        if self.left < self.forceScope.left:
            self.left = self.forceScope.left
        if self.top < self.forceScope.top:
            self.top = self.forceScope.top
        if self.left+self.width > self.forceScope.left+self.forceScope.width:
            self.left -= (self.left+self.width) - (self.forceScope.left+self.forceScope.width)
        if self.top+self.height > self.forceScope.top+self.forceScope.height:
            self.top -= (self.top+self.height) - (self.forceScope.top+self.forceScope.height)


class imgObject(pygame.Surface):

    def __init__(self, width, height, sx, sy, imageName=None):
        super().__init__((width, height), pygame.SRCALPHA) #good!! I deal it
        
        tmpRect = self.get_rect()
        locationRect = Rect(0, 0, 640, 480)
        self.rect = robustRect( locationRect, tmpRect.left, tmpRect.top, tmpRect.width, tmpRect.height)

        self.cursor = Cursor()

        self.rect.top = sy
        self.rect.left = sx

        self.moveRect = pygame.Rect(
            self.rect.left+20,
            self.rect.top+20,
            self.rect.width-40,
            self.rect.height-40)

                
        if imageName != None:
            self.imageName = imageName
            self.image = pygame.image.load(imageName)
            self.setImg(self.image)
        else:
            self.fill((0,0,0,100),(0,0,self.rect.width, self.rect.height))
            self.fill((255,255,255,100), (20,20,self.moveRect.width,self.moveRect.height))
            
        
        self.pressedInMoveRn = False
        self.pressedInResizeRn = False
        self.posRecorder = tuplePos()


    def setImg(self, img):
        ''' here use (0,0) because it blit in itself'''
        self.blit( pygame.transform.scale(img, (self.rect.width, self.rect.height)), (0,0) )


    def present(self, mainSurface):
        mainSurface.blit( pygame.transform.scale(self, (self.rect.width, self.rect.height)), self.getPos() )
        


    def getPos(self):
        return self.rect.topleft

    def getRect(self):
        return self.rect

    def mouseButtonUP(self):
        self.pressedInMoveRn = False
        self.pressedInResizeRn = False

    def mouseButtonDown(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.moveRect.collidepoint(pos) == False:
                self.pressedInResizeRn = True
            else:
                self.pressedInMoveRn = True
            self.posRecorder.setStartPos(pos)
            

    def mouseMove(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.moveRect.collidepoint(pos) == False:
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            else:
                self.cursor.setCursor('move')
        else:
            self.cursor.setCursor('arrow')
        
        if self.pressedInMoveRn:
            delX, delY = self.posRecorder.getDelta(pos)

            self.rect.move_ip(delX, delY)
            self.rect.forceInside()

            self.moveRect = pygame.Rect(
            self.rect.left+20,
            self.rect.top+20,
            self.rect.width-40,
            self.rect.height-40)
            
            
        if self.pressedInResizeRn:
            delX, delY = self.posRecorder.getDelta(pos)

            self.rect.width += delX
            self.rect.height += delY
            self.rect.forceInside()

            self.moveRect = pygame.Rect(
            self.rect.left+20,
            self.rect.top+20,
            self.rect.width-40,
            self.rect.height-40)
            


if __name__ == "__main__":
    obj = App(860,640)
    obj.run()

    
            
            