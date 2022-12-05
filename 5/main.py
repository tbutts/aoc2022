import os
import sys
import re
from typing import List,Dict,Set,Any,Type
from copy import deepcopy
from collections import deque

Stack = List[Type[str]]

def parse_init(puzzle: str) -> List[Stack]:
    # I don't want to deal with this, I'll just cheat
    return 0

def solve(stacks: List[Stack], puzzle: str, callback) -> str:
    stacks = deepcopy(stacks) # dont blow up the lists for future runs
    lines = puzzle[puzzle.find('move'):].splitlines()
    for line in lines:
        (moves, src, dest) = map(int, re.findall(r"\d+", line))
        src -= 1
        dest -= 1
        callback(stacks, moves, src, dest)

    return ''.join([s.pop() for s in stacks])

def part1(stacks, puzzle):
    """After the rearrangement procedure completes, what crate ends up on top of each stack?"""
    def cb(stacks, moves, src, dest):
        for _ in range(moves):
            stacks[dest].append(stacks[src].pop())
    return solve(stacks, puzzle, cb)

def part2(stacks: List[Stack], puzzle: str):
    """[Upgraded] After the rearrangement procedure completes, what crate ends up on top of each stack?"""
    def cb(stacks, moves, src, dest):
        stacks[dest].extend(stacks[src][-moves:])
        stacks[src] = stacks[src][:-moves]
    return solve(stacks, puzzle, cb)

# run test with `watchexec -c -- python3 -m unittest -v main`
import unittest
class TestPuzzle(unittest.TestCase):
    SAMPLE = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
    SAMPLE_STACKS = [
        list('ZN'),
        list('MCD'),
        list('P'),
    ]
    def testa(self):
        a = part1(self.SAMPLE_STACKS, self.SAMPLE)
        self.assertEqual(a, "CMZ")
    
    def testb(self):
        b = part2(self.SAMPLE_STACKS, self.SAMPLE)
        self.assertEqual(b, "MCD")


# just used some hacky bash/python to transpose the file then pull out the strings as python
# shameless, quickly written, hardcoding!
P_STACKS = list(map(list, [
    'PFMQWGRT',
    'HFR',     
    'PZRVGHSD',
    'QHPBFWG', 
    'PSMJH',   
    'MZTHSRPL',
    'PTHNML',  
    'FDQR',    
    'DSCNLPH',
]))

if __name__ == '__main__':
    puzzle: str = open(sys.argv[1]).read()
    print(part1(P_STACKS, puzzle))
    print(part2(P_STACKS, puzzle))
