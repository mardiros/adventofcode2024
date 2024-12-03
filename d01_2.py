import pathlib
from collections import defaultdict

codes = pathlib.Path("d01.py".txt").read_text()

list1, list2 = [], defaultdict(int)
for line in codes.strip().splitlines():
    a, b = line.split()
    list1.append(int(a))
    list2[int(b)] += 1

list1.sort()

dist = 0
while list1:
    a = list1.pop()
    dist += abs(a * list2[a])

print(dist)
