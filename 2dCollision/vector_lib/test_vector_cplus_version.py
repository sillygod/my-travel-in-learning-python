import unittest
from vector import Vector


class TestVector(unittest.TestCase):

    """
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

        self.assertEqual(v1+v2, v3)

    def test_sub_vector(self):
        v1 = Vector(2, 3)
        v2 = Vector(3, 4)
        v3 = Vector(5, 7)

        self.assertEqual(v1, v3-v2)

    def test_mul_vector(self):
        v1 = Vector(2, 2)
        v2 = Vector(1, 3)

        self.assertEqual(Vector(4, 4), v1*2)
        # really, OMG! swig rocks
        self.assertEqual(8, v1*v2)

    def test_vector_length(self):

        v1 = Vector(3, 4)
        self.assertEqual(v1.length(), 5)

    def test_vector_normalize(self):

        v1 = Vector(6, 8)

        v1.normalize()

        self.assertTrue(Vector(6, 8)==v1*10)
