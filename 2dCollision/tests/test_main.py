from __future__ import division
import unittest
from main import Enviromment
from main import Particle
from elements_lib.cElements import Vector


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


class testParticle(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_momentum(self):
        p = Particle(3, 4, 3, 4, 15)
        self.assertEqual(p.momentum, Vector(3, 4))

    def test_be_clicked(self):
        p = Particle(3, 4, 3, 4, 15)
        self.assertTrue(p.isBeClicked(6, 6))

    def test_Kinetic(self):
        p = Particle(3, 4, 3, 4, 15)
        self.assertEqual(25/2, p.calKinetic())

    def test_collision(self):
        """test two particle and check the kinetic whether
        is the same as the state before collision
        """
        pass


