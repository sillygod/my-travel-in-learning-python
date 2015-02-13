import unittest
from main import Vector
from main import Enviromment


class testVector(unittest.TestCase):

    """test function of vector
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_neg_vector(self):

        res = -Vector(2, 2)
        self.assertEqual(-2, res['x'])
        self.assertEqual(-2, res['y'])

    def test_add_vector(self):

        v1 = Vector(2, 3)
        v2 = Vector(1, 2)

        res = v1 + v2
        self.assertEqual(res, Vector(3, 5))

    def test_sub_vector(self):

        v1 = Vector(3, 3)
        v2 = Vector(1, 1)

        self.assertEqual(Vector(2, 2), v1 - v2)

    def test_scale_vector(self):
        """here, we test for division and multiplication
        """
        v1 = Vector(1, 1)
        v2 = Vector(5, 5)
        v3 = v2 / 2

        self.assertEqual(v1 * 5, v2)
        self.assertEqual(v1, v2 / 5)
        self.assertEqual(v3, Vector(2.5, 2.5))

    # below start to test in place calculations
    def test_iadd_vector(self):

        v1 = Vector(2, 2)
        v2 = Vector(3, 3)
        v1 += v2

        self.assertEqual(v1, Vector(5, 5))

    def test_isub_vector(self):

        v1 = Vector(5, 5)
        v2 = Vector(2, 2)

        v1 -= v2

        self.assertEqual(v1, Vector(3, 3))

    def test_inplace_scale_vector(self):

        v1 = Vector(2, 2)
        v1 *= 2

        self.assertEqual(v1, Vector(4, 4))
        v1 /= 2
        self.assertEqual(v1, Vector(2, 2))


class testEnvironment(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_boundRegion(self):
        env = Enviromment()
        env.boundregion = (0, 0, 200, 200)

        self.assertEqual(0, env.boundregion.x)
        self.assertEqual(0, env.boundregion.y)
        self.assertEqual(200, env.boundregion.width)
        self.assertEqual(200, env.boundregion.height)