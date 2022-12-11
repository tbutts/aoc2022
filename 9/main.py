import io
import sys
from collections import deque, defaultdict, Counter
from typing import List,Dict,Set,Any,TextIO,Type,Tuple,Union
from copy import deepcopy
from dataclasses import dataclass

@dataclass
class Pt:
    x: int
    y: int

def move(p: Pt, dir: str):
    match dir:
        case "R":
            p.x += 1
        case "U":
            p.y += 1
        case "L":
            p.x -= 1
        case "D":
            p.y -= 1
        case ERR:
            raise Exception(f"Ground control, there's something wrong: {p=} {ERR=}")

def follow(h: Pt, t: Pt):
    # look. there's a way to cleanup this logic. but I don't wanna.
    dist = abs(h.x - t.x) + abs(h.y - t.y)
    if dist >= 3:
        h_dir = "R" if h.x > t.x else "L"
        v_dir = "U" if h.y > t.y else "D"
        move(t, h_dir)
        move(t, v_dir)
    elif dist == 2:
        if h.x != t.x and h.y != t.y:
            pass
        else:
            if h.x > t.x:
                t.x += 1
            elif h.x < t.x:
                t.x -= 1
            elif h.y > t.y:
                t.y += 1
            elif h.y < t.y:
                t.y -= 1

def solve(puzzle: TextIO, num_knots: int) -> int:
    # make a list of knots
    # track last knot
    # simulate move/follow between all of them
    # try not to get really angry
    # maybe print it visually when you done

    knots = [Pt(0,0) for _ in range(num_knots)]

    m = {}

    for line in puzzle:
        (dir, steps) = line.split()

        # print(f"{dir=} {steps=}; {h=} {t=}")
        if not line:
            break

        for _ in range(int(steps)):
            move(knots[0], dir)  # head always moves
            for k in range(1, len(knots)):
                follow(knots[k-1], knots[k])

            #track the positions tail has been
            tail = knots[-1]
            m[(tail.x, tail.y)] = True

    #print(m.keys())
    return len(m.keys())

def part1(puzzle) -> int:
    """How many positions were visted by the tail?"""
    return solve(puzzle, num_knots=2)

def part2(puzzle) -> int:
    """Now there's 10 knots, how many positions does the tail go to?"""
    return solve(puzzle, num_knots=10)

import unittest
class TestPuzzle(unittest.TestCase):

    def test1(self):
        SAMPLE = """ \
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
        ans = part1(io.StringIO(SAMPLE.strip()))
        self.assertEqual(ans, 13)

    def test2(self):
        SAMPLE = """ \
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
        ans = part2(io.StringIO(SAMPLE.strip()))
        self.assertEqual(ans, 36)

if __name__ == '__main__':
    with open(sys.argv[1]) as puzzle:
        print(part1(puzzle))
    with open(sys.argv[1]) as puzzle:
        print(part2(puzzle))
