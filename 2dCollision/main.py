'''
    find some concept tutorial site
    http://www.euclideanspace.com/physics/dynamics/collision/twod/
    physics

    http://www.petercollingridge.co.uk/pygame-physics-simulation/gravitational-attraction
    http://www.pygame.org/docs/ref/pygame.html

    http://docs.python.org/3.2/library/operator.html
    http://www.rafekettler.com/magicmethods.html
    operator python 3.2



    a physics simulation..

    F = ma
    v = at
    x = vt
    three basic formula

    intend: a snow animation
'''

# from __future__ import division
# __future__ must be at the beginning of file
import pygame

try:
    import pygame._view  # well this line for cx_feeze...
except:
    pass

from pygame.locals import *
import pygame.time
import sys
import math
import random
from elements_lib.pyelements import Vector, Circle
# from elements_lib.elements import Vector, Circle


class Rect(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Particle(object):

    def __init__(self, x=0, y=0, vx=0.0, vy=0.0, size=0, mass=1):
        self.velocity = Vector(vx, vy)
        self.mass = mass
        self.boundCircle = Circle(x, y, size)

    def setMovable(self):
        self.mass -= 1000000

    def setUnMovable(self):
        self.mass += 1000000

    @property
    def momentum(self):
        return self.mass * self.velocity

    def isBeClicked(self, x, y):
        l = (self.boundCircle.pos - Vector(x, y)).length()
        if l < self.boundCircle.radius:
            # be clicked, set v to zero
            self.velocity = Vector(0, 0)
            self.boundCircle.pos.point = (x, y)
            self.setUnMovable()
            return True

        return False

    def calKinetic(self):
        return 0.5 * self.mass * (self.velocity.length() ** 2)

    def collision(self, obj):
        '''
            2d collision -- split in two part
            first -- v parallel to the line connected the two circle center

            second -- v vertical to the line connected the two circle center
            inelastic case, both will has the same velocity....

            v1' = (m1-m2)v1/(m1+m2) + 2 m2v2/(m1+m2)

            v2' = (2m1)v1/(m1+m2) + (m2-m1)v2/(m1+m2)

        '''
        if self.boundCircle.isCollision(obj.boundCircle):  # compare two circle

            p1 = obj.boundCircle.pos - self.boundCircle.pos
            v1, v2 = self.velocity, obj.velocity
            v1L, v2L = self.velocity.length(), obj.velocity.length()

            try:
                rad1 = math.acos(v1.dot(p1) / (p1.length() * v1L))
            except:
                rad1 = 0
            try:
                rad2 = math.acos(v2.dot(-p1) / (p1.length() * v2L))
            except:
                rad2 = 0

            v1 = p1.normalize() * v1L * math.cos(rad1)
            v2 = -p1.normalize() * v2L * math.cos(rad2)

            m1, m2 = self.mass, obj.mass

            v1f = (m1 - m2) * v1 / (m1 + m2) + 2 * m2 * v2 / (m1 + m2)
            v2f = 2 * m1 * v1 / (m1 + m2) + (m2 - m1) * v2 / (m1 + m2)

            self.velocity = v1f + (self.velocity - v1)
            obj.velocity = v2f + (obj.velocity - v2)

    def update(self, dt):
        # self.velocity*dt = Vector(dx,dy)
        self.boundCircle.pos += (self.velocity * dt)


class Enviromment(object):

    '''
        boundregion should be set here
    '''

    def __init__(self):
        self._boundRegion = None
        self.ptList = []

    def getkneticEnergy(self):
        tk = 0
        for obj in self.ptList:
            tk += obj.calKinetic()
        return tk

    def addParticle(self, obj):
        self.ptList.append(obj)

    def present(self, hdc):
        for obj in self.ptList:
            pygame.draw.circle(
                hdc, (255, 255, 255), obj.boundCircle.pos(), int(obj.boundCircle.radius), 0)

    def particleBeClicked(self, x, y):
        ''' return the object be clicked'''
        for obj in self.ptList:
            if obj.isBeClicked(x, y):
                return obj
        return None

    def update(self, dt):

        for index, obj in enumerate(self.ptList):
            for sobj in self.ptList[index + 1:]:
                obj.collision(sobj)
        #[ [obj.collision(sobj) for sobj in self.ptList[index+1:]] for index, obj in enumerate(self.ptList)]

        for obj in self.ptList:
            obj.update(dt)
            self.forceInside(obj)

    def forceInside(self, obj):
        if(obj.boundCircle.pos['x'] - obj.boundCircle.radius) < self._boundRegion.x:
            obj.boundCircle.pos[
                'x'] = self._boundRegion.x + obj.boundCircle.radius
            obj.velocity = obj.velocity.reflect(Vector(1, 0))
        if(obj.boundCircle.pos['x'] + obj.boundCircle.radius) > self._boundRegion.width:
            obj.boundCircle.pos[
                'x'] = self._boundRegion.width - obj.boundCircle.radius
            obj.velocity = obj.velocity.reflect(Vector(1, 0))
        if(obj.boundCircle.pos['y'] - obj.boundCircle.radius) < self._boundRegion.y:
            obj.boundCircle.pos[
                'y'] = self._boundRegion.y + obj.boundCircle.radius
            obj.velocity = obj.velocity.reflect(Vector(0, 1))
        if(obj.boundCircle.pos['y'] + obj.boundCircle.radius) > self._boundRegion.height:
            obj.boundCircle.pos[
                'y'] = self._boundRegion.height - obj.boundCircle.radius
            obj.velocity = obj.velocity.reflect(Vector(0, 1))

    @property
    def boundregion(self):
        return self._boundRegion

    @boundregion.setter
    def boundregion(self, value):
        self._boundRegion = Rect(*value)


def stress_test(env):
    for i in range(150):
        x = random.randint(0, 400)
        y = random.randint(0, 400)
        vx = random.randint(-6, 6)
        vy = random.randint(-6, 6)
        size = random.randint(5, 8)
        env.addParticle(Particle(x, y, vx, vy, size, size * 0.8))


def two_particle_test(env):
    env.addParticle(Particle(20, 20, 10, 30, 25, 15*0.7))
    env.addParticle(Particle(60, 70, 15, 20, 30, 10))


class App(object):

    def __init__(self, width, height):
        pygame.init()
        self.fullScreen = False
        self.hWndDC = pygame.display.set_mode(
            (width, height), self.fullScreen, 32)
        self.winInfo = pygame.display.Info()
        self.selectedObj = None

        self.env = Enviromment()
        self.env.boundregion = (
            0, 0, self.winInfo.current_w, self.winInfo.current_h)

        # two_particle_test(self.env)
        stress_test(self.env)

    def start(self):
        # it seems that it will start the timer when it be created
        self.timer = pygame.time.Clock()
        while True:
            self.timer.tick(30)
            pygame.display.set_caption(
                'fps:{} K:{}'.format(round(self.timer.get_fps(), 2), self.env.getkneticEnergy()))
            self.eventQueue()
            self.update()
            self.present()

    def eventQueue(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_f:
                    pass
            if event.type == pygame.KEYUP:
                if event.key == K_f:
                    pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.x, self.y = pygame.mouse.get_pos()
                self.selectedObj = self.env.particleBeClicked(self.x, self.y)

            if event.type == pygame.MOUSEBUTTONUP:
                if self.selectedObj:
                    self.selectedObj.setMovable()
                self.selectedObj = None

    def update(self):
        dt = 1

        if self.selectedObj:
            x, y = pygame.mouse.get_pos()
            self.selectedObj.velocity = Vector(x - self.x, y - self.y)
            self.x, self.y = x, y

        self.env.update(dt)

    def present(self):
        self.hWndDC.fill((0, 0, 0))
        self.env.present(self.hWndDC)
        pygame.display.update()


if __name__ == '__main__':
    app = App(400, 400)
    app.start()
