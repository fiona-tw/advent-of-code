from setuptools import setup

setup(
    name='aoc_23_solutions',
    version='0.1.0',
    packages=['aoc_23_solutions', 'aoc_23_solutions.tests'],
    url='https://github.com/fiona-tw/advent-of-code/tree/main/advent-of-code-2023/setup.py',
    license='',
    author='Fiona Tahta-Wraith',
    author_email='fionatw@outlook.com',
    description='My attempt at solving the puzzles in Advent of Code 2023',
    entry_points={
        'console_scripts': ['aoc_23_run_puzzle = aoc_23_solutions.run_puzzle:main'],
    },
    setup_requires=[
        'pytest-runner',
        'flake8',
    ],
    tests_require=[
        'pytest',
        'ipdb',
    ],
)
