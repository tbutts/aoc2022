import os
import sys
from typing import List,Dict,Set,Any

def part1(puzzle: str) -> [int, int]:
    lines = puzzle.splitlines()

    c_full_overlap = 0
    c_partial_overlap = 0

    for line in lines:
        (a1,a2,b1,b2) = map(int, line.replace('-', ',').split(',') )
        if (
            (b1 <= a1 and a2 <= b2) or \
            (a1 <= b1 and b2 <= a2)
        ):
            c_full_overlap += 1
            c_partial_overlap += 1
            continue

        if (
            ((b1 <= a1 <= b2) or (b1 <= a2 <= b2)) or \
            ((a1 <= b1 <= a2) or (a1 <= b2 <= a2))
        ):
            c_partial_overlap += 1

    return [c_full_overlap, c_partial_overlap]

def part2(puzzle):
    return 0

# run test with `watchexec -c -- python3 -m unittest -v main`
import unittest
class TestPuzzle(unittest.TestCase):
    SAMPLE = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
    def test(self):
        [a, b] = part1(self.SAMPLE)
        self.assertEqual(a, 2)
        self.assertEqual(b, 4)


if __name__ == '__main__':
    puzzle: List[str] = open(sys.argv[1]).read()
    print(part1(puzzle))
