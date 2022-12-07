import sys
from typing import List,Dict,Set,Any,Union,Type
from copy import deepcopy

def solve(puzzle: str):
    lines = puzzle.splitlines()

    root: Dict = {"/": {}}
    parents = []
    cwd = root

    for line in lines:
        cmd = line.split()
        match cmd:
            case ["$", "cd", "/"]:
                cwd = root["/"]
                parents.clear()
            case ["$", "cd", ".."]:
                cwd = parents.pop() if len(parents) else cwd
            case ["$", "cd", folder]:
                parents.append(cwd)
                # i guess, everything is just mkdir + cd. We never list the same dir twice, so make this easy
                cwd[folder] = {}
                cwd = cwd[folder]
            case ["$", "ls"]:
                pass

            # only "listings" aren't preceeded by "$"
            case ["dir", foldername]:
                cwd[foldername] = {}
            case [num, filename]:
                cwd[filename] = int(num)

    """
    Find all of the directories with a total size of at most 100000.
    What is the sum of the total sizes of those directories?
    """
    MAX_DIR_SIZE  = 100000


    # recursive reducer (would be much cleaner in lisp/clojure/js/rust/anything functional with lambdas)
    totals_under_limit = []
    totals = []
    def bad_du(folder: Dict) -> int:
        total = 0
        for v in folder.values():
            if isinstance(v, int):
                total += v
            else:
                total += bad_du(v)

        # this is the "real" return.
        if total <= MAX_DIR_SIZE:
            totals_under_limit.append(total)

        totals.append(total)

        return total

    bad_du(root)
    # print(f"{totals_under_limit=}, ")
    p1 = sum(totals_under_limit)

    """
    Find the smallest directory that, if deleted, would free up enough space
    on the filesystem to run the update.
    What is the total size of that directory?
    """
    MAX_DISK_SIZE = 70000000
    SPACE_NEEDED  = 30000000

    totals.sort(reverse=False)
    disk_used = totals[-1]  # last dir sorted is "/" root
    best = totals[0]
    for t in totals:
        # print(f"{disk_used=} {t=} ? {(MAX_DISK_SIZE - SPACE_NEEDED)=}")
        if disk_used - t <= MAX_DISK_SIZE - SPACE_NEEDED:
            best = t
            break
    
    return (p1, best)

import unittest
class TestPuzzle(unittest.TestCase):
    def test1(self):
        sample = """ \
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
        (p1, p2) = solve(sample)
        self.assertEqual(p1, 95437)
        self.assertEqual(p2, 24933642)


if __name__ == '__main__':
    puzzle: str = open(sys.argv[1]).read()
    (p1, p2) = solve(puzzle)
    print(p1)
    print(p2)
