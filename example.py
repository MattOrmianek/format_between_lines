"""Example module."""
import subprocess

def two_sum_better(nums: list, target: int) -> list:
    num_to_index = {}
    for index, number in enumerate(nums):
        complement = target - number
        if complement in num_to_index:
            return [num_to_index[complement], index]
        num_to_index[number] = index

def test_function(f):
    nums = [2, 7, 11, 15]
    target = 9
    assert f(nums, target) == [0, 1], "Test case 1 failed"

    nums = [3, 2, 4]
    target = 6
    assert f(nums, target) == [1, 2], "Test case 2 failed"

    nums = [3, 3]
    target = 6
    assert f(nums, target) == [0, 1], "Test case 3 failed"

    nums = [1, 2]
    target = 10
    assert f(nums, target) is None, "Test case 4 failed"

    nums = [10, 11, 18, 19]
    target = 37
    assert f(nums, target) == [2, 3], "Test case 5 failed"
test_function(two_sum_better)
