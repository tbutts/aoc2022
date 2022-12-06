import os
import sys
import re
from typing import List,Dict,Set,Any,Type
from copy import deepcopy


def solve(puzzle: str, pattern_size: int) -> int:
    sz = pattern_size
    for i in range(sz, len(puzzle)):
        if len(set(puzzle[i-sz:i])) == sz:
            return i

    raise Exception("No marker found!")

def part1(puzzle: str) -> int:
    """How many characters need to be processed before the first start-of-packet marker is detected?"""
    return solve(puzzle, pattern_size=4)

def part2(puzzle: str) -> int:
    """How many characters need to be processed before the first start-of-message marker is detected?"""
    return solve(puzzle, pattern_size=14)

# run test with `watchexec -c -- python3 -m unittest -v main`
import unittest
class TestPuzzle(unittest.TestCase):

    def test1(self):
        tests = [
            ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
            ("nppdvjthqldpwncqszvftbrmjlhg", 6),
            ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
            ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
        ]
        for test in tests:
            self.assertEqual(part1(test[0]), test[1], test[0])

    def test2(self):
        tests = [
                ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
                ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
                ("nppdvjthqldpwncqszvftbrmjlhg", 23),
                ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
                ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26),
        ]
        for test in tests:
            self.assertEqual(part2(test[0]), test[1], test[0])


if __name__ == '__main__':
    puzzle: str = open(sys.argv[1]).read()
    print(part1(puzzle))
    print(part2(puzzle))
