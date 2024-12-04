from solutions.logic.day_1 import get_distance_sum, get_similarity_score


def test_get_distance_sum():
    example_input = """3   4
4   3
2   5
1   3
3   9
3   3"""
    assert get_distance_sum(example_input) == 11


def test_get_similarity_score():
    example_input = """3   4
4   3
2   5
1   3
3   9
3   3"""
    assert get_similarity_score(example_input) == 31
