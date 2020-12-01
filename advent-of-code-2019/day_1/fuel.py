#!/usr/bin/env python3
import math
import sys
from typing import List, NamedTuple


class Module(NamedTuple):
    mass: float

class CounterUpper:
    def __init__(self, modules: List[Module]):
        self.modules = modules

    def calculate_fuel(self, mass: float) -> float:
        return math.floor(mass / 3.0) - 2.0

    def _fuel_for_module(self, module: Module) -> float:
        fuel_for_module = self.calculate_fuel(module.mass)
        fuel_for_fuel = self.calculate_fuel(fuel_for_module)
        extra_fuel = fuel_for_fuel
        while extra_fuel > 0:
            fuel_for_module += extra_fuel
            extra_fuel = self.calculate_fuel(extra_fuel)
        return fuel_for_module

    def required_fuel(self) -> float:
        return sum([self._fuel_for_module(module) for module in self.modules])


def get_counter_for_masses(masses: List[float]) -> CounterUpper:
    modules = [Module(mass) for mass in masses]
    return CounterUpper(modules)

def get_required_fuel_for_masses(masses: List[float]) -> float:
    
    counter = get_counter_for_masses(masses)
    return counter.required_fuel()


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        masses_str = f.read()
        masses = [float(mass) for mass in masses_str.split("\n") if mass]
        total_fuel = get_required_fuel_for_masses(masses)
    print(f"Fuel requirements for all modules: {total_fuel}")
