import unittest
from elements_lib.cElements import Vector
from elements_lib.cElements import Circle


class TestVector(unittest.TestCase):

    """here test the vector implemented by c++
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_declare_vector(self):
        v1 = Vector(2, 3, 4)

        self.assertEqual(v1.x, 2)
        self.assertEqual(v1.y, 3)
        self.assertEqual(v1.z, 4)

    def test_add_vector(self):
        v1 = Vector(2, 3)
        v2 = Vector(3, 4)
        v3 = Vector(5, 7)

        self.assertEqual(v1 + v2, v3)

    def test_sub_vector(self):
        v1 = Vector(2, 3)
        v2 = Vector(3, 4)
        v3 = Vector(5, 7)

        self.assertEqual(v1, v3 - v2)

    def test_div_vector(self):
        v1 = Vector(5, 5)
        v2 = v1/3

        self.assertEqual(v1 / 3, v2)

    def test_mul_dot_vector(self):
        v1 = Vector(2, 2)
        v2 = Vector(1, 3)

        self.assertEqual(Vector(4, 4), v1 * 2)
        # really, OMG! swig rocks
        self.assertEqual(8, v1 * v2)
        self.assertEqual(8, v1.dot(v2))

    def test_vector_length(self):

        v1 = Vector(3, 4)
        self.assertEqual(v1.length(), 5)

    def test_vector_normalize(self):

        v1 = Vector(6, 8)
        normalize_v1 = v1.normalize()
        print(normalize_v1)  # why get 0.600xxxx 0.800xxxx

        self.assertTrue(v1 == normalize_v1 * 10)

    def test_vector_neg(self):
        v1 = Vector(1, 1)

        self.assertEqual(Vector(-1, -1), -v1)

    def test_vector_reflect(self):

        v1 = Vector(1, 1)
        n = Vector(0, 1)

        self.assertEqual(Vector(1, -1), v1.reflect(n))

    def test_getitem_vector(self):
        v = Vector(2, 3)
        self.assertEqual(2, v['x'])

    def test_setitem_vector(self):
        v = Vector(0, 3)
        v['x'] = 5
        self.assertEqual(5, v['x'])

    def test_call_vactor(self):
        v = Vector(5.3, 2.2)
        # call will return int value
        self.assertEqual(5, v()[0])
        self.assertEqual(2, v()[1])


class TestCircle(unittest.TestCase):

    """
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_Circle(self):

        c = Circle(2, 2, 3)
        self.assertEqual(Vector(2, 2), c.pos)
        self.assertEqual(3, c.radius)

    def test_isCollision(self):

        c1 = Circle(0, 0, 3)
        c2 = Circle(1, 1, 1)

        self.assertEqual(True, c1.isCollision(c2))
        self.assertEqual(Vector(4, 4), c2.pos)
