# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.5
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from __future__ import division
import math

from sys import version_info
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_elements', [dirname(__file__)])
        except ImportError:
            import _elements
            return _elements
        if fp is not None:
            try:
                _mod = imp.load_module('_elements', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _elements = swig_import_helper()
    del swig_import_helper
else:
    import _elements
del version_info
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.


def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr_nondynamic(self, class_type, name, static=1):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    if (not static):
        return object.__getattr__(self, name)
    else:
        raise AttributeError(name)

def _swig_getattr(self, class_type, name):
    return _swig_getattr_nondynamic(self, class_type, name, 0)


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object:
        pass
    _newclass = 0


class Vector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Vector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Vector, name)
    __repr__ = _swig_repr
    __swig_setmethods__["x"] = _elements.Vector_x_set
    __swig_getmethods__["x"] = _elements.Vector_x_get
    if _newclass:
        x = _swig_property(_elements.Vector_x_get, _elements.Vector_x_set)
    __swig_setmethods__["y"] = _elements.Vector_y_set
    __swig_getmethods__["y"] = _elements.Vector_y_get
    if _newclass:
        y = _swig_property(_elements.Vector_y_get, _elements.Vector_y_set)
    __swig_setmethods__["z"] = _elements.Vector_z_set
    __swig_getmethods__["z"] = _elements.Vector_z_get
    if _newclass:
        z = _swig_property(_elements.Vector_z_get, _elements.Vector_z_set)

    def __init__(self, x=0, y=0, z=0):
        this = _elements.new_Vector(x, y, z)
        try:
            self.this.append(this)
        except:
            self.this = this

    def __call__(self):
        """ return an int tuple"""
        if math.isnan(self.x):
            return (0, 0)

        return (int(self.x), int(self.y))

    def __neg__(self):
        """ negative a vector """
        return Vector(-self.x, -self.y)

    def __getitem__(self, value):
        return Vector.__getattr__(self, value)

    def __setitem__(self, index, value):
        Vector.__setattr__(self, index, value)

    def __str__(self):
        return 'Vector x={} y={} z={}'.format(self.x, self.y, self.z)

    def __add__(self, v2):
        return _elements.Vector___add__(self, v2)

    def __sub__(self, v2):
        return _elements.Vector___sub__(self, v2)

    def __rmul__(self, *args):
        return _elements.Vector___mul__(self, *args)

    def __mul__(self, *args):
        return _elements.Vector___mul__(self, *args)

    def __div__(self, rhs):
        return _elements.Vector___mul__(self, 1/rhs)

    def __ne__(self, v2):
        return _elements.Vector___ne__(self, v2)

    def __eq__(self, v2):
        return _elements.Vector___eq__(self, v2)

    @property
    def point(self):
        return (self.x, self.y)

    @point.setter
    def point(self, value):
        self.x = value[0]
        self.y = value[1]

    @property
    def angle(self):
        """ return radian  """
        try:
            return math.atan(self.y/self.x)
        except:
            return math.pi/2

    def reflect(self, normal):
        """
        """
        I = self
        self = (2*(-I.dot(normal))*normal)+I
        return self

    def length(self):
        return _elements.Vector_length(self)

    def dot(self, v2):
        return _elements.Vector___mul__(self, v2)

    def normalize(self):
        v = Vector(self.x, self.y, self.z)
        _elements.Vector_normalize(v)
        return v

    def rotate(self, radius):
        newx = self.x * math.cos(radius) - self.y * math.sin(radius)
        newy = self.x * math.sin(radius) + self.y * math.cos(radius)
        return Vector(newx, newy)
    __swig_destroy__ = _elements.delete_Vector
    __del__ = lambda self: None
Vector_swigregister = _elements.Vector_swigregister
Vector_swigregister(Vector)

class Circle(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Circle, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Circle, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _elements.new_Circle(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def isCollision(self, c):
        return _elements.Circle_isCollision(self, c)
    __swig_setmethods__["pos"] = _elements.Circle_pos_set
    __swig_getmethods__["pos"] = _elements.Circle_pos_get
    if _newclass:
        pos = _swig_property(_elements.Circle_pos_get, _elements.Circle_pos_set)
    __swig_setmethods__["radius"] = _elements.Circle_radius_set
    __swig_getmethods__["radius"] = _elements.Circle_radius_get
    if _newclass:
        radius = _swig_property(_elements.Circle_radius_get, _elements.Circle_radius_set)
    __swig_destroy__ = _elements.delete_Circle
    __del__ = lambda self: None
Circle_swigregister = _elements.Circle_swigregister
Circle_swigregister(Circle)

# This file is compatible with both classic and new-style classes.


