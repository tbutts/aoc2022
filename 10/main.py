import io
import sys
from collections import deque, defaultdict, Counter
from typing import List,Dict,Set,Any,TextIO,Type,Tuple,Union
from copy import deepcopy
from dataclasses import dataclass


def part1(puzzle: TextIO) -> int:
    """What's the signal strength?"""
    rx = 1  # register X
    cycle = 1
    prog_stack: Tuple[int, str, int] | None = None

    sum_signal_readings = 0

    while True:
        if (cycle + 20) % 40 == 0:
            signal_str = cycle * rx
            sum_signal_readings += signal_str

        if prog_stack is not None:
            rx += prog_stack[2]
            prog_stack = None
        else:
            match puzzle.readline().strip().split():
                case ["addx", num]:
                    prog_stack = (cycle + 2, "add", int(num))
                case ["noop"]:
                    pass
                case _: # EOF
                    break

        cycle += 1

    print(f"{rx=} {sum_signal_readings=}")
    return sum_signal_readings

HEIGHT = 6
WIDTH = 40

@dataclass
class Point:
    x: int
    y: int

def part2(puzzle: TextIO) -> str:
    """What are the 8 capital letters shown on the CRT after your instructions run?"""
    rx = 1  # register X
    cycle = 1
    prog_stack: Tuple[int, str, int] | None = None

    crt = []
    for y in range(HEIGHT):
        crt.append([])
        for _ in range(WIDTH):
            crt[y].append('')

    while True:
        if cycle > HEIGHT * WIDTH:
            break

        # check rx sprite position, see if it overlaps with cpu cycle
        draw_pos = Point(x=((cycle - 1) % 40), y=((cycle - 1) // 40))
        draw_ch = '.'
        if (rx - 1) <= (draw_pos.x) <= (rx + 1):
            draw_ch = '#'
        #print(f"c={cycle} Drawing: {draw_pos=} {rx=} {draw_ch=}")
        crt[draw_pos.y][draw_pos.x] = draw_ch

        if prog_stack is not None:
            rx += prog_stack[2]
            prog_stack = None
        else:
            match puzzle.readline().strip().split():
                case ["addx", num]:
                    prog_stack = (cycle + 2, "add", int(num))
                case ["noop"]:
                    pass
                case _: # EOF
                    break

        cycle += 1

    # draw the crt
    img = '\n'.join([''.join(line) for line in crt])
    return img


import unittest
class TestPuzzle(unittest.TestCase):

    def test1(self):
        SAMPLE = """ \
noop
addx 3
addx -5
"""
        part1(io.StringIO(SAMPLE.strip()))

    def test2(self):
        with open("test_input.txt") as f:
            self.assertEqual(part1(f), 13140)

    def test3(self):
        IMG = """ \
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
""".strip()
        with open("test_input.txt") as f:
            self.assertEqual(part2(f), IMG)


if __name__ == '__main__':
    with open(sys.argv[1]) as puzzle:
        print(part1(puzzle))
    with open(sys.argv[1]) as puzzle:
        print(part2(puzzle))
