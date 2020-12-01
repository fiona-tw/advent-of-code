import unittest
from parameterized import parameterized

from fuel import CounterUpper, Module


class TestFuelCounterUpper(unittest.TestCase):
    
    @staticmethod
    def get_module(mass):
        return Module(mass=mass)

    @parameterized.expand([
        (12, 2),
        (14, 2),
        (1969, 966),
        (100756, 50346),
    ])
    def test_individual_module_fuel_requirements(self, mass, expected_fuel):
        module = self.get_module(mass)
        required_fuel = CounterUpper([module])._fuel_for_module(module)
        self.assertEqual(required_fuel, expected_fuel)

    def test_total_fuel_requirements(self):
        expected_total_fuel = 51316
        test_masses = [12, 14, 1969, 100756]
        modules = [Module(mass) for mass in test_masses]
        counter = CounterUpper(modules)
        required_total_fuel = counter.required_fuel()
        self.assertEqual(required_total_fuel, expected_total_fuel)

