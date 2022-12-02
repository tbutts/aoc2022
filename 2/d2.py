import os
import sys

lines = open(sys.argv[1]).readlines()

# we can only use the most coy solutions to define simple data
r = [
    [3, 6, 0],
    [0, 3, 6],
    [6, 0, 3],
]
rr = [{k:v for k,v in zip('XYZ', vec_x)} for vec_x in r]
rrr = {k:v for k,v in zip('ABC', rr)}
print(f"{rrr=  }")


s = [
    [3, 1, 2],
    [1, 2, 3],
    [2, 3, 1],
]
ss = [{k:v for k,v in zip('XYZ', vec_x)} for vec_x in s]
sss = {k:v for k,v in zip('ABC', ss)}

shape_score = {abc: num+1 for num,abc in enumerate('XYZ')}
shape_score2 = {abc: num for num,abc in zip([0,3,6], 'XYZ')}

# this code is extra terrible

score = 0
score2 = 0
for line in lines:
    (them, us) = line.strip().split(" ")
    score += rrr[them][us]
    score += shape_score[us]
    
    score2 += sss[them][us]
    score2 += shape_score2[us]

print(f"{score= }")
print(f"{score2=}")
print()

