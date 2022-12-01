import os
import sys
import pathlib

lines = pathlib.Path(sys.argv[1]).open().readlines()
elves = []
curr = 0
for line in lines:
    if line == "\n":
        elves.append(curr)
        curr = 0
        continue

    c = int(line)
    curr += c
elves.append(curr)

elves.sort(reverse=True)
print()
print(f"{elves[0]= }")
# print(f"{elves=}")
print(f"{elves[0:3]= }")
print(f"{sum(elves[0:3])= }")