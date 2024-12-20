from setuptools import setup
from setuptools.config.expand import find_packages

setup(
    name="aoc_24_solutions",
    version="0.1.0",
    packages=find_packages(include=["solutions", "solutions.*"]),
    url="https://github.com/fiona-tw/advent-of-code/tree/main/advent-of-code-2024/setup.py",
    license="",
    author="Fiona Tahta-Wraith",
    author_email="fionatw@outlook.com",
    description="My attempt at solving the puzzles in Advent of Code 2024",
    entry_points={
        "console_scripts": ["run_puzzle_aoc_24 = solutions.run_puzzle:run"],
    },
    setup_requires=[
        "pytest-runner",
        "flake8",
    ],
    tests_require=[
        "pytest",
        "ipdb",
    ],
)
