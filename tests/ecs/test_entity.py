import unittest

from src.ecs.entity import Entity

class TestEntity(unittest.TestCase):
    def test_get_gets_last_set_component(self):
        e = Entity('b', (0, 0, 128))
        expected = HealthComponent(42)
        unexpected = HealthComponent(10)

        e.set(unexpected)
        self.assertEqual(e.get(HealthComponent), unexpected)

        e.set(expected)
        self.assertEqual(e.get(HealthComponent), expected)        


class HealthComponent:
    def __init__(self, health):
        self.health = health
        self.total_health = health