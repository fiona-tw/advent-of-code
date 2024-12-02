from solutions.logic.day_1 import get_distance_sum

def test_example_input():
   example_input = """
3   4
4   3
2   5
1   3
3   9
3   3
"""
   assert get_distance_sum(example_input) == 11
