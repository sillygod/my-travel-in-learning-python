from __future__ import division
import math


class Vector(object):

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __call__(self):
        ''' return an int tuple '''
        return (int(self.x), int(self.y))

    def __neg__(self):
        ''' ex. -Vector(2,2) -> Vector(-2,-2)'''
        return Vector(-self.x, -self.y)

    def __eq__(self, rhs):
        ''' for comparison two vector is the same or not '''
        return (self.x == rhs.x) and (self.y == rhs.y)

    # def __del__(self):
    #   print('vector {} is delete'.format(self.point))

    def __getitem__(self, value):
        return self.__dict__[value]

    def __setitem__(self, index, value):
        self.__dict__[index] = value

    def __add__(self, rhs):
        return Vector(self.x + rhs.x, self.y + rhs.y)

    def __div__(self, rhs):
        if isinstance(rhs, Vector):
            raise ValueError
        return Vector(self.x / rhs, self.y / rhs)

    def __truediv__(self, rhs):
        if isinstance(rhs, Vector):
            raise ValueError
        return Vector(self.x // rhs, self.y // rhs)

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


class Circle(object):

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
