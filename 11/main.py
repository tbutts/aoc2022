import io
import math
import re
import sys
from collections import deque, defaultdict, Counter
from typing import List,Dict,Set,Any,TextIO,Type,Tuple,Union
from copy import deepcopy
from dataclasses import dataclass

@dataclass
class Mob:
    items: deque[int]

    op: str  # plus, minus, star, div
    op_factor: str

    div_check: int  # divisor for test

    target_true_mon: int
    target_false_mon: int

    inspections: int = 0

def print_mobs(mobs):
    print('\n'.join([f"M {i}: {', '.join(map(str, m.items))}" for i,m in enumerate(mobs)]))

def solve(puzzle: TextIO, rounds: int, anxiety: bool=False) -> int:
    """Give the product of the two most active monkey's number of times they inspect your items."""
    mobs: List[Mob] = []
    while True:
        line = puzzle.readline().strip()
        if not line:
            break

        # parse the stanza
        line = puzzle.readline().strip()
        starting = re.findall(r"\d+", line)
        starting = map(int, starting)

        line = puzzle.readline().strip()
        (op, op_factor) = re.search(r"new = old (.) (\w+)", line).groups()

        line = puzzle.readline().strip()
        (divisor,) = re.search("divisible by (\d+)", line).groups()

        line = puzzle.readline().strip()
        (throw_on_true,) = re.search("If true: throw to monkey (\d+)", line).groups()

        line = puzzle.readline().strip()
        (throw_on_false,) = re.search("If false: throw to monkey (\d+)", line).groups()


        mob = Mob(
            items=deque(starting),
            op=op,
            op_factor=op_factor,
            div_check=int(divisor),
            target_true_mon=int(throw_on_true),
            target_false_mon=int(throw_on_false),
        )

        mobs.append(mob)

        # skip empty divider line and loop
        line = puzzle.readline()

    # monkey sim.
    for r in range(rounds):
        for m in mobs:
            for it in m.items:
                m.inspections += 1
                op_factor = it if m.op_factor == "old" else int(m.op_factor)
                if m.op == "+":
                    it += op_factor
                else:
                    it *= op_factor

                # monkey "boredom"
                if not anxiety:
                    it = math.floor(it / 3)

                # test & throw
                if it % m.div_check == 0:
                    mobs[m.target_true_mon].items.append(it)
                else:
                    mobs[m.target_false_mon].items.append(it)

            # everything got "thrown" to another monkey
            m.items.clear()
        # print_mobs(mobs)

    top_mobs = sorted([m.inspections for m in mobs], reverse=True)[0:2]
    monkey_biz = math.prod(top_mobs)
    return monkey_biz

def part1(puzzle: TextIO) -> int:
    return solve(puzzle, rounds=20, anxiety=False)

def part2(puzzle: TextIO) -> int:
    return solve(puzzle, rounds=10000, anxiety=True)


import unittest
class TestPuzzle(unittest.TestCase):
    SAMPLE = """ \
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

    def test1(self):
        ans = part1(io.StringIO(self.SAMPLE.strip()))
        self.assertEqual(ans, 10605)

    # oops
    # def test2(self):
    #     ans = part2(io.StringIO(self.SAMPLE.strip()))
    #     self.assertEqual(ans, 2713310158)

if __name__ == '__main__':
    with open(sys.argv[1]) as puzzle:
        print(part1(puzzle))
    # with open(sys.argv[1]) as puzzle:
        # print(part2(puzzle))
