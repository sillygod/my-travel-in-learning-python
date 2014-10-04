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


class Vector:

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __call__(self):
        ''' return an int tuple '''
        return (int(self.x), int(self.y))

    def __neg__(self):
        ''' ex. -Vector(2,2) -> Vector(-2,-2)'''
        return Vector(-self.x, -self.y)

    # def __del__(self):
    #   print('vector {} is delete'.format(self.point))

    def __getitem__(self, value):
        return self.__dict__[value]

    def __setitem__(self, index, value):
        self.__dict__[index] = value

    def __add__(self, rhs):
        return Vector(self.x + rhs.x, self.y + rhs.y)

    def __truediv__(self, rhs):
        if isinstance(rhs, Vector):
            raise ValueError
        return Vector(self.x / rhs, self.y / rhs)

    def __mul__(self, rhs):
        ''' rhs is a pure num '''
        if isinstance(rhs, Vector):
            raise ValueError
        return Vector(self.x * rhs, self.y * rhs)

    def __rmul__(self, lhs):
        return Vector(self.x * lhs, self.y * lhs)

    def __sub__(self, rhs):
        return Vector(self.x - rhs.x, self.y - rhs.y)

    def __imul__(self, rhs):
        '''
            *= equals to assign and inplace calculation
            ex. a *= b --> a = operator.imul(a, b)
        '''
        if isinstance(rhs, Vector):
            raise ValueError
        self.x *= rhs
        self.y *= rhs
        return self

    def __itruediv__(self, rhs):
        if isinstance(rhs, Vector):
            raise ValueError
        self.x /= rhs
        self.y /= rhs
        return self

    def __iadd__(self, rhs):
        self.x += rhs.x
        self.y += rhs.y
        return self

    def __isub__(self, rhs):
        self.x -= rhs.x
        self.y -= rhs.y
        return self

    def __str__(self):
        return 'vector x ={} y={}'.format(self.x, self.y)

    @property
    def point(self):
        return (self.x, self.y)

    @point.setter
    def point(self, value):
        self.x = value[0]
        self.y = value[1]

    @property
    def angle(self):
        ''' return radian'''
        try:
            return math.atan(self.y / self.x)
        except:
            return math.pi / 2  # tan(math.pi/2) almost unlimeted big

    def reflect(self, normal):
        '''
            I <  |---->normal
               \ | /
             ___\|/____

             2*(-I.dot(normal)) -- scalar
        '''
        I = self
        self = (2 * (-I.dot(normal)) * normal) + I
        return self

    def normalVector(self):
        ''' return the normal vector of self'''
        l = self.length()
        angle = self.angle + math.pi / 2
        return Vector(l * math.cos(angle), l * math.sin(angle))

    def normalize(self):
        try:
            length = self.length()
            return Vector(self.x / length, self.y / length)
        except:
            return self

    def rotate(self, radius):
        newx = self.x * math.cos(radius) - self.y * math.sin(radius)
        newy = self.x * math.sin(radius) + self.y * math.cos(radius)
        return Vector(newx, newy)

    def length(self):
        return math.hypot(self.x, self.y)  # math.sqrt(self.x**2 + self.y**2)

    def dot(self, v2):
        if isinstance(v2, Vector):
            return self.x * v2.x + self.y * v2.y
        else:
            raise ValueError


class Circle:

    def __init__(self, x, y, r):
        ''' public data '''
        self.pos = Vector(x, y)
        self.radius = r

    def __str__(self):
        return 'x:{} y:{} r:{}'.format(self.pos['x'], self.pos['y'], self.radius)

    def isCollision(self, circle):
        v = circle.pos - self.pos
        if v.length() < self.radius + circle.radius:
            ''' collision then, adjust the position to make no overlapped'''
            circle.pos = self.pos + \
                v.normalize() * (self.radius + circle.radius)
            # self.pos = circle.pos - v.normalize()*(self.radius+circle.radius)
            return True

        return False


class Rect:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Particle:

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


class Enviromment:

    '''
        boundregion should be set here
    '''

    def __init__(self):
        self._boundRegion = None
        self.ptList = []

    def addParticle(self, obj):
        self.ptList.append(obj)

    def present(self, hdc):
        for obj in self.ptList:
            pygame.draw.circle(
                hdc, (255, 255, 255), obj.boundCircle.pos(), obj.boundCircle.radius, 0)

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


class App:

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

        for i in range(150):
            x = random.randint(0, 400)
            y = random.randint(0, 400)
            vx = random.randint(-6, 6)
            vy = random.randint(-6, 6)
            size = random.randint(3, 5)
            self.env.addParticle(Particle(x, y, vx, vy, size, size * 0.8))

    def start(self):
        # it seems that it will start the timer when it be created
        self.timer = pygame.time.Clock()
        while True:
            self.timer.tick(30)
            pygame.display.set_caption(
                '{}'.format(round(self.timer.get_fps(), 2)))
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
