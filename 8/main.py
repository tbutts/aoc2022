import io
import sys
from collections import defaultdict, Counter
from typing import List,Dict,Set,Any, TextIO,Type
from copy import deepcopy

def part1(puzzle: TextIO) -> int:
    """How many trees are visible from outside the grid?"""
    grid = []
    for line in puzzle.readlines():
        line = line.strip()
        if len(line) > 0:
            grid.append([int(ch) for ch in line])

    grid_t = [list(l) for l in zip(*grid)]

    vis_counter = 0
    for y in range(1, len(grid)-1):
        for x in range(1, len(grid[y])-1):
            tree = grid[y][x]
            # left
            if tree > max([t for t in grid[y][:x]]):
                vis_counter += 1
                continue
            # right
            elif tree > max([t for t in grid[y][x+1:]]):
                vis_counter += 1
                continue
            # up
            elif tree > max([t for t in grid_t[x][:y]]):
                vis_counter += 1
                continue
            # down
            elif tree > max([t for t in grid_t[x][y+1:]]):
                vis_counter += 1
                continue

    # add always-visible edges. Perimeter
    vis_counter += ((len(grid) + len(grid_t)) * 2) - 4

    return vis_counter

def part2(puzzle: TextIO) -> int:
    """Best scenic score possible for any tree?"""
    grid = []
    for line in puzzle.readlines():
        line = line.strip()
        if len(line) > 0:
            grid.append([int(ch) for ch in line])

    grid_t = [list(l) for l in zip(*grid)]

    best_scene = 0
    for y in range(1, len(grid)-1):
        for x in range(1, len(grid[y])-1):
            tree = grid[y][x]

            left = 0
            for dx in range(x-1, -1, -1):
                left += 1
                if grid[y][dx] >= tree:
                    break
            right = 0
            for dx in range(x+1, len(grid[y])):
                right += 1
                if grid[y][dx] >= tree:
                    break
            up = 0
            for dy in range(y-1, -1, -1):
                up += 1
                if grid_t[x][dy] >= tree:
                    break
            down = 0
            for dy in range(y+1, len(grid_t[x])):
                down += 1
                if grid_t[x][dy] >= tree:
                    break

            vis_score = left * up * right * down
            best_scene = max(best_scene, vis_score)

    return best_scene


import unittest
class TestPuzzle(unittest.TestCase):
    SAMPLE = """ \
30373
25512
65332
33549
35390
"""

    def test1(self):
        f = io.StringIO(self.SAMPLE)
        self.assertEqual(part1(f), 21)

    def test2(self):
        f = io.StringIO(self.SAMPLE)
        self.assertEqual(part2(f), 8)


if __name__ == '__main__':
    puzzle = open(sys.argv[1])
    print(part1(puzzle))
    puzzle.seek(0)
    print(part2(puzzle))
